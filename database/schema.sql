-- ============================================================
-- Mini-Trello - MySQL database setup script
-- Run this once to create the database and the tasks table.
--   mysql -u root -p < schema.sql
-- Then set DATABASE_URL in backend/.env to:
--   mysql+pymysql://root:your_password@localhost:3306/mini_trello
-- ============================================================

CREATE DATABASE IF NOT EXISTS mini_trello
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mini_trello;

CREATE TABLE IF NOT EXISTS tasks (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'todo',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT ck_task_status CHECK (status IN ('todo', 'in_progress', 'done'))
) ENGINE=InnoDB;