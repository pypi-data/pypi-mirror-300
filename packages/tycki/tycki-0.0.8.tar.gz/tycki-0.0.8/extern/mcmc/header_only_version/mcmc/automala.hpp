/*################################################################################
  ##
  ##   Copyright (C) 2024 Richard D. Paul
  ##
  ##   This file is largely built upon code from the MCMC C++ library by Keith O'Hara,
  ##   majorly altered by Richard D. Paul as part of the tycki sampling library.
  ##
  ##   Licensed under the Apache License, Version 2.0 (the "License");
  ##   you may not use this file except in compliance with the License.
  ##   You may obtain a copy of the License at
  ##
  ##       http://www.apache.org/licenses/LICENSE-2.0
  ##
  ##   Unless required by applicable law or agreed to in writing, software
  ##   distributed under the License is distributed on an "AS IS" BASIS,
  ##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ##   See the License for the specific language governing permissions and
  ##   limitations under the License.
  ##
  ################################################################################*/
 
/*
 * Metropolis-adjusted Langevin algorithm
 */

#ifndef _mcmc_automala_HPP
#define _mcmc_automala_HPP


/**
 * @brief The Metropolis-adjusted Langevin Algorithm (MALA)
 *
 * @param initial_vals a column vector of initial values.
 * @param target_log_kernel the log posterior kernel function of the target distribution, taking three arguments:
 *   - \c vals_inp a vector of inputs; and
 *   - \c grad_out a vector to store the gradient; and
 *   - \c target_data additional data passed to the user-provided function.
 * @param draws_out a matrix of posterior draws, where each row represents one draw.
 * @param target_data additional data passed to the user-provided function.
 *
 * @return a boolean value indicating successful completion of the algorithm.
 */ 

bool
automala(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel, 
    Mat_t& draws_out, 
    void* target_data
);

/**
 * @brief The Metropolis-adjusted Langevin Algorithm (MALA)
 *
 * @param initial_vals a column vector of initial values.
 * @param target_log_kernel the log posterior kernel function of the target distribution, taking three arguments:
 *   - \c vals_inp a vector of inputs; and
 *   - \c grad_out a vector to store the gradient; and
 *   - \c target_data additional data passed to the user-provided function.
 * @param draws_out a matrix of posterior draws, where each row represents one draw.
 * @param target_data additional data passed to the user-provided function.
 * @param settings parameters controlling the MCMC routine.
 *
 * @return a boolean value indicating successful completion of the algorithm.
 */ 

bool
automala(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel, 
    Mat_t& draws_out, 
    void* target_data, 
    algo_settings_t& settings
);


namespace internal
{

bool
automala_impl(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel, 
    Mat_t& draws_out, 
    void* target_data, 
    algo_settings_t* settings_inp
);

#include "mala.ipp"

}

//



//

inline
bool
internal::automala_impl(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel, 
    Mat_t& draws_out, 
    void* target_data, 
    algo_settings_t* settings_inp
)
{
    bool success = false;

    const size_t n_vals = BMO_MATOPS_SIZE(initial_vals);

    //
    // MALA settings

    algo_settings_t settings;

    if (settings_inp) {
        settings = *settings_inp;
    }

    const size_t n_burnin_draws = settings.automala_settings.n_burnin_draws;
    const size_t n_keep_draws   = settings.automala_settings.n_keep_draws;
    const size_t n_adapt_draws   = settings.automala_settings.n_adapt_draws;
    const size_t n_total_draws  = n_burnin_draws + n_keep_draws;

    fp_t eps_init = settings.automala_settings.step_size;

    const Mat_t precond_matrix = (BMO_MATOPS_SIZE(settings.automala_settings.precond_mat) == n_vals*n_vals) ? settings.automala_settings.precond_mat : BMO_MATOPS_EYE(n_vals);
    const Mat_t sqrt_precond_matrix = BMO_MATOPS_CHOL_LOWER(precond_matrix);
    const Mat_t identity = BMO_MATOPS_EYE(n_vals);
    Mat_t rand_precond_matrix = sqrt_precond_matrix;

    const bool vals_bound = settings.vals_bound;
    
    const ColVec_t lower_bounds = settings.lower_bounds;
    const ColVec_t upper_bounds = settings.upper_bounds;

    const ColVecInt_t bounds_type = determine_bounds_type(vals_bound, n_vals, lower_bounds, upper_bounds);

    //rand_engine_t rand_engine(settings.rng_seed_value);
    rand_engine_t& rand_engine = settings.rand_engine;

    // parallelization setup

#ifdef MCMC_USE_OPENMP
    int omp_n_threads = 1;
    
    if (settings.automala_settings.omp_n_threads > 0) {
        omp_n_threads = settings.automala_settings.omp_n_threads;
    } else {
        omp_n_threads = std::max(1, static_cast<int>(omp_get_max_threads()) / 2); // OpenMP often detects the number of virtual/logical cores, not physical cores
    }
#endif

    //
    // lambda functions for box constraints

    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* box_data)> box_log_kernel 
        = [target_log_kernel, vals_bound, bounds_type, lower_bounds, upper_bounds] 
        (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data) 
        -> fp_t 
    { // 
        if (vals_bound) {
            ColVec_t vals_inv_trans = inv_transform(vals_inp, bounds_type, lower_bounds, upper_bounds);

            return target_log_kernel(vals_inv_trans, nullptr, target_data) + log_jacobian(vals_inp, bounds_type, lower_bounds, upper_bounds);
        } else {
            return target_log_kernel(vals_inp, nullptr, target_data);
        }
    };

    // std::tie(new_draw, new_momentum, prop_LP) = leap_frog(prev_draw, momentum, rand_precond_matrix, eps)
    std::function<std::tuple<ColVec_t, ColVec_t, fp_t> (const ColVec_t&, void*, const ColVec_t&, const Mat_t&, const fp_t)> leap_frog 
        = [target_log_kernel, vals_bound, bounds_type, lower_bounds, upper_bounds] 
        (const ColVec_t& x, void* target_data, const ColVec_t& p, const Mat_t& M, const fp_t eps) 
        -> std::tuple<ColVec_t, ColVec_t, fp_t>
    { // 
        const size_t n_vals = BMO_MATOPS_SIZE(x);
        ColVec_t x_prime (n_vals);
        ColVec_t p_prime (n_vals);
        ColVec_t grad(n_vals);

        if (vals_bound) {
            throw std::runtime_error("Bounds not yet supported for autoMALA.");
        } else {
            // eq. 2 from https://proceedings.mlr.press/v238/biron-lattes24a.html
            target_log_kernel(x, &grad, target_data);
            p_prime = p + .5 * eps * grad;
            x_prime = x + eps * M.llt().solve(p_prime);

            fp_t logp = target_log_kernel(x_prime, &grad, target_data);
            p_prime = p_prime + .5 * eps * grad;

            return {x_prime, -p_prime, logp};
        }
    };

    std::function<std::tuple<fp_t, fp_t, ColVec_t, ColVec_t, fp_t> 
        (const ColVec_t&, const ColVec_t&, fp_t, fp_t, fp_t, fp_t, void*, const Mat_t&)> select_step_size
    = [leap_frog, target_log_kernel] 
        (const ColVec_t& x, const ColVec_t& p, fp_t a, fp_t b, fp_t eps_init, fp_t logp, void* target_data, const Mat_t& M) 
        -> std::tuple<fp_t, fp_t, ColVec_t, ColVec_t, fp_t>
    { //
        fp_t eps = eps_init;
        fp_t logp_prime;
        ColVec_t x_prime;
        ColVec_t p_prime;

        std::tie(x_prime, p_prime, logp_prime) = leap_frog(x, target_data, p, M, eps);
        fp_t ell = logp_prime - logp + gaussian_log_density(p_prime, M) - gaussian_log_density(p, M);
        int delta = (ell >= std::log(b) ? 1 : 0) - (ell <= std::log(a) ? 1 : 0);
        size_t j = 0;

        if (delta == 0) {
            return {eps_init, j, x_prime, p_prime, logp_prime};
        }

        size_t i = 0;
        while (true && i < 10e9) { // ewwwww
            i += 1; // just a little safety measure

            eps *= std::pow(2, delta);
            j += delta;

            std::tie(x_prime, p_prime, logp_prime) = leap_frog(x, target_data, p, M, eps);
            ell = logp_prime - logp + gaussian_log_density(p_prime, M) - gaussian_log_density(p, M);
            //delta = (ell >= std::log(b) ? 1 : 0) - (ell <= std::log(a) ? 1 : 0);

            if (delta > 0 && ell < std::log(b)) {
                eps *= .5;
                std::tie(x_prime, p_prime, logp_prime) = leap_frog(x, target_data, p, M, eps);
                return {eps, j-1, x_prime, p_prime, logp_prime};
            } else if (delta < 0 && ell > std::log(a)) {
                return {eps, j, x_prime, p_prime, logp_prime};
            }
        }
    };

    //
    // setup
    
    ColVec_t first_draw = initial_vals;

    if (vals_bound) { // should we transform the parameters?
        first_draw = transform(initial_vals, bounds_type, lower_bounds, upper_bounds);
    }

    BMO_MATOPS_SET_SIZE(draws_out, n_keep_draws, n_vals);

    fp_t prev_LP = box_log_kernel(first_draw, nullptr, target_data);
    fp_t prop_LP = prev_LP;
    
    ColVec_t prev_draw = first_draw;
    ColVec_t new_draw  = first_draw;

    //

    size_t n_accept = 0;
    ColVec_t rand_vec(n_vals);

    ColVec_t prev_momentum(n_vals);
    ColVec_t new_momentum(n_vals);

    fp_t u_1;
    fp_t u_2;
    
    fp_t z;

    fp_t eps;
    size_t j;

    fp_t eps_rev;
    size_t j_rev;

    fp_t a;
    fp_t b;

    fp_t alpha;

    for (size_t draw_ind = 0; draw_ind < n_total_draws; ++draw_ind) {
        // draw rv eta from 0-1-inflated beta distribution, which basically means to either choose 0, 1 or a
        // number from the (0, 1) interval uniformly at random
        fp_t eta = 1;
        
        // form random preconditioning matrix by setting eta * sqrt_precond + (1 - eta)
        rand_precond_matrix = eta * sqrt_precond_matrix + (1 - eta) * identity;
        
        // sample momentum from N(0, C) with C being the randomized preconditioner
        bmo::stats::internal::rnorm_vec_inplace<fp_t>(n_vals, rand_engine, rand_vec);
        prev_momentum = rand_precond_matrix * rand_vec;

        // sample soft bounds (a, b) from [0, 1]^2 s.t. a < b
        u_1 = bmo::stats::runif<fp_t>(rand_engine);
        u_2 = bmo::stats::runif<fp_t>(rand_engine);

        a = std::min(u_1, u_2);
        b = std::max(u_1, u_2);
        
        // call the step size selector. this internally also already performs the leap frog step
        std::tie(eps, j, new_draw, new_momentum, prop_LP) = select_step_size(prev_draw, prev_momentum, a, b, eps_init, 
                                                                             prev_LP, target_data, rand_precond_matrix);

        // perform round based tuning if we're still in unadj phase
        if (draw_ind < n_adapt_draws) { 

        } else {
            // perform the reversibility check
            std::tie(eps_rev, j_rev, std::ignore, std::ignore, std::ignore) = select_step_size(new_draw, new_momentum, a, b, eps_init,
                                                                                               prop_LP, target_data, rand_precond_matrix);

            // check the metropolis criterion, augmented by the outcome of the reversibility check
            alpha = prop_LP - prev_LP + gaussian_log_density(new_momentum, rand_precond_matrix) - gaussian_log_density(prev_momentum, rand_precond_matrix);
            z = bmo::stats::runif<fp_t>(rand_engine);

            if (j == j_rev && std::log(z) < alpha) {
                prev_draw = new_draw;
                prev_LP = prop_LP;

                if (draw_ind >= n_burnin_draws) {
                    draws_out.row(draw_ind - n_burnin_draws) = BMO_MATOPS_TRANSPOSE(new_draw);
                    n_accept++;
                }
            } else {
                if (draw_ind >= n_burnin_draws) {
                    draws_out.row(draw_ind - n_burnin_draws) = BMO_MATOPS_TRANSPOSE(prev_draw);
                }
            }
        }
    }

    success = true;

    //

    if (vals_bound) {
#ifdef MCMC_USE_OPENMP
        #pragma omp parallel for num_threads(omp_n_threads)
#endif
        for (size_t draw_ind = 0; draw_ind < n_keep_draws; ++draw_ind) {
            draws_out.row(draw_ind) = inv_transform<RowVec_t>(draws_out.row(draw_ind), bounds_type, lower_bounds, upper_bounds);
        }
    }

    if (settings_inp) {
        settings_inp->automala_settings.n_accept_draws = n_accept;
    }

    //

    return success;
}

// wrappers

inline
bool
automala(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel, 
    Mat_t& draws_out, 
    void* target_data
)
{
    return internal::automala_impl(initial_vals,target_log_kernel,draws_out,target_data,nullptr);
}

inline
bool
automala(
    const ColVec_t& initial_vals, 
    std::function<fp_t (const ColVec_t& vals_inp, ColVec_t* grad_out, void* target_data)> target_log_kernel,
    Mat_t& draws_out, 
    void* target_data, 
    algo_settings_t& settings
)
{
    return internal::automala_impl(initial_vals,target_log_kernel,draws_out,target_data,&settings);
}

#endif
