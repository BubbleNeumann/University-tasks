fn part2(func: fn(&Vec<f64>) -> f64, x0: &mut Vec<f64>, i: usize, j: usize) -> f64 {
    0.
}

fn hessian(func: fn(&Vec<f64>) -> f64, x0: &mut Vec<f64>) -> Vec<Vec<f64>> {
    let size = x0.len();
    let mut hes = vec![vec![0.; size]; size];
    let (mut row, mut col): (usize, usize);
    for ind in 0..size * size {
        (row, col) = (ind / size, ind % size);
        hes[row][col] = part2(func, x0, row, col);
    }

    hes
}
fn main() {}
