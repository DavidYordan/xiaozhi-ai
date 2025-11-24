CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS categories (
  id uuid PRIMARY KEY,
  name text,
  description text,
  summary text,
  embedding vector(1536),
  embed_model text,
  embed_dim integer,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS categories_embedding_cos_idx ON categories USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS items (
  id uuid PRIMARY KEY,
  role text,
  summary text,
  embedding vector(1536),
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS items_embedding_cos_idx ON items USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS resources (
  id uuid PRIMARY KEY,
  url text,
  local_path text,
  modality text,
  caption text,
  embedding vector(1536),
  embed_model text,
  embed_dim integer,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS resources_embedding_cos_idx ON resources USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS relations (
  id uuid PRIMARY KEY,
  item_id uuid REFERENCES items(id),
  category_id uuid REFERENCES categories(id)
);

CREATE INDEX IF NOT EXISTS relations_item_idx ON relations(item_id);
CREATE INDEX IF NOT EXISTS relations_category_idx ON relations(category_id);
