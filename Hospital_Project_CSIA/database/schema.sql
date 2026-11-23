-- Initial normalized schema for fictional health education lectures.
CREATE DATABASE IF NOT EXISTS hospital_education
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_education;

CREATE TABLE IF NOT EXISTS lectures (
  lecture_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  speaker VARCHAR(150) NOT NULL,
  department VARCHAR(120) NOT NULL,
  lecture_date DATE NOT NULL,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  video_location VARCHAR(500) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
  tag_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS topics (
  topic_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS lecture_tags (
  lecture_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (lecture_id, tag_id),
  FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS lecture_topics (
  lecture_id INT NOT NULL,
  topic_id INT NOT NULL,
  PRIMARY KEY (lecture_id, topic_id),
  FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE CASCADE,
  FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);
