--
-- 转存表中的数据 `student`
--

INSERT INTO `student` (`student_id`, `department`,`email`,`student_name`,`moodle`) VALUES
(6666666666, 'BSc(DA)', 'Chloe_appleid@outlook.com', 'Max Lee','https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=Z_MYELEARNING');

--
-- 转存表中的数据 `login_record`
--

-- INSERT INTO `login_record` (`student_id`, `behaviour_id`, `login_time`, `logout_time`, `duration`) VALUES



--
-- 转存表中的数据 `coursebase`
--

INSERT INTO `coursebase` (`c_code`, `c_title`, `message`,`c_zoom_link`) VALUES
('ECON2280-1A','Introductory econometrics','Looking for RA next semester!','https://moodle.hku.hk/course/view.php?id=101626'),
('COMP3278-1A','Introduction to database management systems','Feel free to make appointment of  office hours with me.','https://moodle.hku.hk/course/view.php?id=96513'),
('MATH2211-1A','Multivariable calculus','Remember to prepare for required calculator.','https://moodle.hku.hk/course/view.php?id=98724'),
('STAT2602-1A','Probability and statistics II','The lectures will not be recorded this semester.','https://moodle.hku.hk/course/view.php?id=100183');

--
-- 转存表中的数据 `courset`
--

INSERT INTO `courset` (`c_code`, `c_day`,`c_time_start`,`c_time_end`,`lecturer`,`tutor`) VALUES
('ECON2280-1A','Mon',093000,122000,'Dr. Clement Wong','Mr. Benyang Wang'),
('COMP3278-1A','Mon',143000,152000,'Mr.Yao Mu','Mr.Yizhou Li'),
('MATH2211-1A','Tue',103000,122000,'Dr. Tak Wing CHING','Mr. Jiaming ZHANG'),
('STAT2602-1A','Tue',133000,162000,'Dr. Dora Y. Zhang','Mr.Harrison Cheung'),
('COMP3278-1A','Thu',133000,152000,'Dr. Ping Luo','Mr.Yizhou Li'),
('MATH2211-1A','Fri',113000,152000,'Dr. Tak Wing CHING','Mr. Jiaming ZHANG');

--
-- 转存表中的数据 `enrolled`
--

INSERT INTO `enrolled` (`student_id`, `c_code` ) VALUES
(6666666666, 'COMP3278-1A'),
(6666666666, 'ECON2280-1A');


--
-- 转存表中的数据 `tutorialbase`
--

INSERT INTO `tutorialbase` (`c_code`,`t_num`,`t_date`, `t_day`, `t_time_start`,  `t_time_end`) VALUES
('ECON2280-1A',1,'2022-11-16','Wed','10:30','11:20'),
('ECON2280-1A',2,'2022-11-17','Wed','10:30','11:20'),
('ECON2280-1A',3,'2022-11-18','Wed','10:30','11:20'),
('COMP3278-1A',1,'2022-11-19','Tue','16:30','17:20'),
('COMP3278-1A',2,'2022-11-20','Tue','16:30','17:20'),
('COMP3278-1A',3,'2022-11-21','Tue','16:30','17:20'),
('MATH2211-1A',1,'2022-11-22','Fri','09:30','10:20'),
('MATH2211-1A',2,'2022-11-23','Fri','09:30','10:20'),
('MATH2211-1A',3,'2022-11-24','Fri','09:30','10:20'),
('STAT2602-1A',1,'2022-11-25','Thu','14:30','15:20'),
('STAT2602-1A',2,'2022-11-26','Thu','14:30','15:20'),
('STAT2602-1A',3,'2022-11-27','Thu','14:30','15:20');

--
-- 转存表中的数据 `coursem`
--

INSERT INTO `coursem` (`c_code`, `c_num`, `c_date`, `c_material_link`) VALUES
('ECON2280-1A',1,'2022-11-14','https://moodle.hku.hk/mod/resource/view.php?id=2685115'),
('ECON2280-1A',2,'2022-11-15','https://moodle.hku.hk/mod/resource/view.php?id=2700008'),
('ECON2280-1A',3,'2022-11-16','https://moodle.hku.hk/mod/resource/view.php?id=2708606'),
('COMP3278-1A',1,'2022-11-17','https://moodle.hku.hk/mod/resource/view.php?id=2665229'),
('COMP3278-1A',2,'2022-11-18','https://moodle.hku.hk/mod/resource/view.php?id=2665229'),
('COMP3278-1A',3,'2022-11-19','https://moodle.hku.hk/mod/resource/view.php?id=2694930'),
('COMP3278-1A',4,'2022-11-20','https://moodle.hku.hk/mod/resource/view.php?id=2694930'),
('COMP3278-1A',5,'2022-11-21','https://moodle.hku.hk/mod/resource/view.php?id=2703589'),
('COMP3278-1A',6,'2022-11-22','https://moodle.hku.hk/mod/resource/view.php?id=2703589'),
('MATH2211-1A',1,'2022-11-23','https://moodle.hku.hk/mod/resource/view.php?id=2672675'),
('MATH2211-1A',2,'2022-11-24','https://moodle.hku.hk/mod/resource/view.php?id=2672675'),
('MATH2211-1A',3,'2022-11-25','https://moodle.hku.hk/mod/resource/view.php?id=2699682'),
('MATH2211-1A',4,'2022-11-26','https://moodle.hku.hk/mod/resource/view.php?id=2699682'),
('MATH2211-1A',5,'2022-11-27','https://moodle.hku.hk/mod/resource/view.php?id=2721078'),
('MATH2211-1A',6,'2022-11-28','https://moodle.hku.hk/mod/resource/view.php?id=2721078'),
('STAT2602-1A',1,'2022-11-29','https://moodle.hku.hk/mod/resource/view.php?id=2690443'),
('STAT2602-1A',2,'2022-11-30','https://moodle.hku.hk/mod/resource/view.php?id=2690444'),
('STAT2602-1A',3,'2022-12-1','https://moodle.hku.hk/mod/resource/view.php?id=2710627');

--
-- 转存表中的数据 `tutorialm`
--

INSERT INTO `tutorialm` (`c_code`, `t_num`, `t_date`, `t_material_link`) VALUES
('ECON2280-1A',1,'2022-11-16','https://moodle.hku.hk/mod/resource/view.php?id=2694255'),
('ECON2280-1A',2,'2022-11-17','https://moodle.hku.hk/mod/resource/view.php?id=2700011'),
('ECON2280-1A',3,'2022-11-18','https://moodle.hku.hk/mod/resource/view.php?id=2714324'),
('COMP3278-1A',1,'2022-11-19','https://moodle.hku.hk/mod/resource/view.php?id=2668112'),
('COMP3278-1A',2,'2022-11-20','https://moodle.hku.hk/mod/resource/view.php?id=2696843'),
('COMP3278-1A',3,'2022-11-21','https://moodle.hku.hk/mod/resource/view.php?id=2709094'),
('MATH2211-1A',1,'2022-11-22','https://moodle.hku.hk/mod/resource/view.php?id=2698690'),
('MATH2211-1A',2,'2022-11-23','https://moodle.hku.hk/mod/resource/view.php?id=2706796'),
('MATH2211-1A',3,'2022-11-24','https://moodle.hku.hk/mod/resource/view.php?id=2716497'),
('STAT2602-1A',1,'2022-11-25','https://moodle.hku.hk/mod/resource/view.php?id=2691957'),
('STAT2602-1A',2,'2022-11-26','https://moodle.hku.hk/mod/resource/view.php?id=2698372'),
('STAT2602-1A',3,'2022-11-27','https://moodle.hku.hk/mod/resource/view.php?id=2707332');

--
-- 转存表中的数据 `DDL`
--

INSERT INTO `DDL` (`c_code`, `name`, `ddl_date`, `ddl_time`,`ddl_submit_link`) VALUES
('ECON2280-1A','Ass1','2022-11-14','23:59','https://moodle.hku.hk/pluginfile.php/4169663/mod_assign/introattachment/0/Assign3.pdf?forcedownload=1'),
('COMP3278-1A','Ass1','2022-11-15','12:00','https://moodle.hku.hk/pluginfile.php/4169663/mod_assign/introattachment/0/Assign3.pdf?forcedownload=1'),
('MATH2211-1A','Exercise1','2022-11-16','23:59','https://moodle.hku.hk/mod/assign/view.php?id=2748732'),
('STAT2602-1A','Exercise1','2022-11-17','23:59','https://moodle.hku.hk/mod/assign/view.php?id=2748732');
