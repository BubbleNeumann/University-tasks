pub const PHI: f64 = 1.61803398874989484820;
pub const EPS: f64 = 0.000_001;
pub const ITERS_MAX: usize = 1_000;

pub fn func1(x: f64) -> f64 {
    x * x
}

pub fn func2(x: f64) -> f64 {
    x * x + 3.0 * x
}

pub fn vec_func(x: &Vec<f64>) -> f64 {
    (x[0] - 5.) * x[0] + (x[1] - 3.) * x[1] // min at point x = 2.5, y = 1.5
}

pub fn bounded_func(args: &Vec<f64>) -> f64 {
    vec_func(args)
        + (1. / (5. - args[0] * 2. + args[1] * 3.))
        + (1. / (6. + args[0] * 3. - args[1]))
}
