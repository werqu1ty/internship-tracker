CREATE TABLE applications (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	company TEXT NOT NULL,
	role TEXT NOT NULL,
	location TEXT,
	deadline TEXT,
	status TEXT NOT NULL DEFAULT 'wishlist' CHECK (status IN ('wishlist', 'applied', 'interview', 'offer', 'rejected')),
	notes TEXT,
	link TEXT,
	source TEXT NOT NULL DEFAULT 'manual',
	source_url TEXT UNIQUE,
	created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
