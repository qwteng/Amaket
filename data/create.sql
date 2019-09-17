CREATE TABLE IF NOT EXISTS t_stock_tob(
   code TEXT  PRIMARY KEY,
   name TEXT,
   price_tob REAL,
   type_tob TEXT,
   uptm TEXT
);
CREATE TABLE IF NOT EXISTS t_tob_track(
   code TEXT,
   name TEXT,
   price_tob REAL,
   open REAL,
   high REAL,
   low REAL,
   close REAL,
   tob REAL,
   premium REAL,
   date TEXT,
   uptm TEXT
);
