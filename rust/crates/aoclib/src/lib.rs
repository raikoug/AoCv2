use std::env;
use std::fs;
use std::io;
use std::path::PathBuf;

/// Prova a trovare la root del repo:
/// - Se esiste l'ENV `AOC_ROOT`, usa quella.
/// - Altrimenti sale dalle cartelle finché trova una directory che contiene `data/`.
pub fn repo_root() -> io::Result<PathBuf> {
    if let Ok(root) = env::var("AOC_ROOT") {
        return Ok(PathBuf::from(root));
    }

    let mut dir = env::current_dir()?;
    loop {
        if dir.join("data").is_dir() {
            return Ok(dir);
        }
        if !dir.pop() {
            // Non abbiamo trovato niente, fallback: current dir iniziale
            return env::current_dir();
        }
    }
}

/// Costruisce il path dell'input:
///   ./data/{year}/day_{day}/input_{part}.txt
pub fn input_path(year: i32, day: u8, part: u8) -> io::Result<PathBuf> {
    let root = repo_root()?;
    let path = root
        .join("data")
        .join(year.to_string())
        .join(format!("day_{:02}", day))
        .join(format!("input_{}.txt", part));

    Ok(path)
}

/// Legge l'input come String.
pub fn read_input(year: i32, day: u8, part: u8) -> io::Result<String> {
    let path = input_path(year, day, part)?;
    fs::read_to_string(path)
}
