use std::collections::{HashMap, HashSet};

fn main() {
    let key = "monarchy";
    let message = "instrumentsz";

    let chars = key.to_uppercase();

    let mut used = HashSet::new();

    let mut ascii: Vec<char> = chars
        .chars()
        .filter(|&c| c.is_ascii_alphabetic())
        .filter(|&c| used.insert(c))
        .collect();

    let alphabets: Vec<char> = (65..91)
        .map(|c| c as u8 as char)
        .filter(|c| *c != 'J')
        .collect();

    let mut matrix = vec![vec![' '; 5]; 5];

    for &c in &alphabets {
        if !used.contains(&c) {
            ascii.push(c);
        }
    }
    let mut char_map: HashMap<char, (usize, usize)> = HashMap::new();

    for (i, &c) in ascii.iter().enumerate() {
        let row = i / 5;
        let col = i % 5;
        matrix[row][col] = c;
        char_map.insert(c, (row, col));
    }

    let prepared_message: String = message
        .to_uppercase()
        .replace(" ", "")
        .replace("J", "I")
        .chars()
        .filter(|&c| c.is_ascii_alphabetic()).collect();

    let mut diagraphs: Vec<(char, char)> = Vec::new();
    let mut i: usize = 0;

    while i < prepared_message.len() {
        let first = prepared_message.chars().nth(i).unwrap();

        if i + 1 >= prepared_message.len() {
            diagraphs.push((first, 'X'));
            i += 2;
            continue;
        }

        let second = prepared_message.chars().nth(i + 1).unwrap();

        if first == second {
            diagraphs.push((first, 'X'));
            i += 1;
            continue;
        }

        diagraphs.push((first, second));

        i += 2;
    }

    let mut encrypted = String::new();

    for graph in diagraphs {
        let (first, second) = graph;
        let pos_one = char_map.get(&first);
        let pos_two = char_map.get(&second);

        if let (Some((row_first, col_first)), Some((row_second, col_second))) = (pos_one, pos_two) {
            if row_first == row_second {
                let col_one = (col_first + 1) % 5;
                let col_two = (col_second + 1) % 5;
                encrypted.push(matrix[*row_first][col_one]);
                encrypted.push(matrix[*row_second][col_two]);
            } else if col_first == col_second {
                let row_one = (row_first + 1) % 5;
                let row_two = (row_second + 1) % 5;
                encrypted.push(matrix[row_one][*col_first]);
                encrypted.push(matrix[row_two][*col_second]);
            } else {
                encrypted.push(matrix[*row_first][*col_second]);
                encrypted.push(matrix[*row_second][*col_first]);
            }
        }
    }
    println!("{encrypted}");
}
