#![allow(dead_code)]
mod common;

use crate::common::*;
use std::mem::swap;

fn bisect(func: fn(f64) -> f64, x1: &mut f64, x2: &mut f64) -> f64 {
    let eps = EPS * 0.1; // for some types of functions bisect requires higher accuracy
    let mut xc = 0.0;
    if x2 < x1 {
        swap(x1, x2)
    }

    for _ in 0..ITERS_MAX {
        xc = (*x1 + *x2) * 0.5;
        if func(xc + eps) > func(xc - eps) {
            *x2 = xc - eps;
        } else {
            *x1 = xc + eps;
        }

        if (*x1 - *x2).abs() < eps {
            break;
        }
    }

    xc
}

fn golden_ratio(func: fn(f64) -> f64, x1: &mut f64, x2: &mut f64) -> f64 {
    let mut xl = 0.0;
    let mut xr = 0.0;
    let mut delta: f64;
    if x1 > x2 {
        swap(x1, x2)
    }

    for _ in 0..ITERS_MAX {
        delta = *x2 - *x1;
        xl = *x2 - delta / PHI;
        xr = *x1 + delta / PHI;
        if func(xl) > func(xr) {
            *x1 = xl;
        } else {
            *x2 = xr;
        }

        if (xl - xr).abs() < EPS {
            break;
        }
    }

    (xr + xl) * 0.5
}

fn fibonacci(func: fn(f64) -> f64, x1: &mut f64, x2: &mut f64) -> f64 {
    fn get_closest_fib_pair(val: f64, f_n: &mut u64, f_n_1: &mut u64) {
        if val < 1.0 {
            return;
        }

        *f_n_1 = 1;

        if val < 2.0 {
            return;
        }

        let mut f_tmp: u64;
        while (*f_n as f64) < val {
            f_tmp = *f_n + *f_n_1;
            (*f_n, *f_n_1) = (*f_n_1, f_tmp);
        }
    }

    if x1 > x2 {
        swap(x1, x2);
    }

    let mut xl: f64 = *x1;
    let mut xr: f64 = *x2;
    let mut f_n: u64 = 0;
    let mut f_n_1: u64 = 0;

    get_closest_fib_pair((xr - xl) / EPS, &mut f_n, &mut f_n_1);

    let mut delta: f64;
    let mut f_tmp: u64;

    for _ in 0..ITERS_MAX {
        if f_n == f_n_1 || (xr - xl) < EPS {
            break;
        }

        delta = xr - xl;
        f_tmp = f_n_1 - f_n;
        xl = *x1 + delta * (f_tmp as f64 / f_n_1 as f64);
        xr = *x1 + delta * (f_n as f64 / f_n_1 as f64);

        (f_n, f_n_1) = (f_tmp, f_n);

        if func(xl) < func(xr) {
            *x2 = xr;
        } else {
            *x1 = xl;
        }
    }

    (*x1 + *x2) * 0.5
}

fn main() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bisect_on_func1() {
        let mut a = 7.0;
        let mut b = -5.0;
        let res = bisect(func1, &mut a, &mut b);
        assert!(res > -EPS && res < EPS);
    }

    #[test]
    fn test_bisect_on_func2() {
        let mut a = -7.0;
        let mut b = 5.0;
        let res = bisect(func2, &mut a, &mut b);
        assert!(res > -1.5 - EPS && res < -1.5 + EPS);
    }

    #[test]
    fn test_golden_ratio_on_func1() {
        let mut a = -5.0;
        let mut b = 8.0;
        let res = golden_ratio(func1, &mut a, &mut b);
        assert!(res > -EPS && res < EPS);
    }

    #[test]
    fn test_golden_ratio_on_func2() {
        let mut a = -5.0;
        let mut b = 0.0;
        let res = golden_ratio(func2, &mut a, &mut b);
        assert!(res > -1.5 - EPS && res < -1.5 + EPS);
    }

    #[test]
    fn test_fibonacci_on_func1() {
        let mut a = 10.;
        let mut b = -1.;
        let res = fibonacci(func1, &mut a, &mut b);
        assert!(res > -0.01 && res < 0.01);
    }

    #[test]
    fn test_fibonacci_on_func2() {
        let mut a = 10.;
        let mut b = -15.;
        let res = fibonacci(func2, &mut a, &mut b);
        assert!(res > -1.5 - EPS && res < -1.5 + EPS);
    }
}
