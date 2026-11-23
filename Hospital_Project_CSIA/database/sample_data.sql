USE hospital_education;

INSERT INTO lectures (lecture_id, title, speaker, department, lecture_date, category, description, video_location) VALUES
(1, 'Understanding Everyday Heart Health', 'Dr. Maya Chen', 'Cardiology', '2025-02-12', 'Prevention', 'A fictional introductory talk about heart healthy habits and routine checkups.', 'videos/heart-health.mp4'),
(2, 'Building a Balanced Plate', 'Jordan Lee, RD', 'Nutrition Services', '2025-03-04', 'Wellness', 'A fictional guide to practical food choices and balanced meals.', 'videos/balanced-plate.mp4'),
(3, 'Getting Better Sleep', 'Dr. Sam Rivera', 'Sleep Medicine', '2025-04-18', 'Wellness', 'A fictional overview of sleep routines and common sleep health questions.', 'videos/sleep-health.mp4'),
(4, 'Managing Blood Sugar', 'Dr. Emily Chen', 'Endocrinology', '2025-05-08', 'Diabetes', 'A fictional introduction to understanding blood sugar and discussing care with a health professional.', NULL),
(5, 'Supporting Mental Wellbeing', 'Dr. Alex Morgan', 'Psychiatry', '2025-06-16', 'Mental Health', 'A fictional talk about everyday wellbeing and finding trusted support.', NULL);

INSERT INTO tags (tag_id, name) VALUES
(1, 'prevention'), (2, 'heart'), (3, 'nutrition'), (4, 'sleep'), (5, 'wellness'),
(6, 'diabetes'), (7, 'blood sugar'), (8, 'mental health'), (9, 'stress management');
INSERT INTO topics (topic_id, name) VALUES
(1, 'healthy habits'), (2, 'cardiovascular health'), (3, 'meal planning'), (4, 'sleep routines'),
(5, 'blood sugar basics'), (6, 'emotional wellbeing');
INSERT INTO lecture_tags (lecture_id, tag_id) VALUES
(1,1),(1,2),(1,5),(2,3),(2,5),(3,4),(3,5),(4,6),(4,7),(5,8),(5,9);
INSERT INTO lecture_topics (lecture_id, topic_id) VALUES
(1,1),(1,2),(2,1),(2,3),(3,1),(3,4),(4,5),(5,6);
