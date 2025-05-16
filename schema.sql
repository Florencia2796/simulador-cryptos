CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    from_moneda TEXT NOT NULL,
    cantidad_from REAL NOT NULL,
    to_moneda TEXT NOT NULL,
    cantidad_to REAL NOT NULL,
    valor_unitario REAL NOT NULL
);
