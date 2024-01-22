CREATE TABLE problems (
    title TEXT,
    slug TEXT,
    num INTEGER
);

CREATE INDEX idx_num ON problems (num);
