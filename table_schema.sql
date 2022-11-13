SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+08:00";

DROP DATABASE IF EXISTS `COMP3278`;
CREATE DATABASE `COMP3278`;
USE `COMP3278`;
-- --------------------------------------------------------

--
-- 表的结构 `Student`
--

CREATE TABLE `student` (
  `student_id` bigint(10) NOT NULL,
  `department` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `student_name` varchar(20) NOT NULL,
  `moodle` varchar(200) NOT NULL
);



-- 表的索引 `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);
-- --------------------------------------------------------

--
-- 表的结构 `login_record`
--

CREATE TABLE `login_record` (
  `student_id` bigint(10) NOT NULL,
  `behaviour_id` int NOT NULL,
  `login_time` TIMESTAMP,
  `logout_time` TIMESTAMP,
  `duration` time
) ;

--
-- 转存表中的数据 `login_record`
--

-- INSERT INTO `login_record` (`student_id`, `behaviour_id`, `login_time`, `logout_time`, `duration`) VALUES

-- 表的索引 `login_record`
--

ALTER TABLE `login_record`
  ADD PRIMARY KEY (`behaviour_id`,`student_id`),
  ADD FOREIGN KEY (`student_id`) REFERENCES student(`student_id`);
-- --------------------------------------------------------

--
-- 表的结构 `add`
--

-- CREATE TABLE `ADD` (
  -- `student_id` bigint(10) NOT NULL,
  -- `event_id` int NOT NULL
-- ) ;

--
-- 转存表中的数据 `add`
--

-- 表的索引 `add`
--

-- ALTER TABLE `add`
  -- ADD FOREIGN KEY (`event_id`) REFERENCES Event(`event_id`),
  -- ADD FOREIGN KEY (`student_id`) REFERENCES student(`student_id`);
-- --------------------------------------------------------

--
-- 表的结构 `event`
--

-- CREATE TABLE `event` (
  -- `event_id` int NOT NULL,
  -- `title` varchar(80) NOT NULL,
  -- `organizer` varchar(80) NOT NULL,
  -- `location` varchar(80) NOT NULL,
  -- `date` date,
  -- `E_time_start` time,
  -- `E_time_end` time
-- );

--
-- 转存表中的数据 `event`
--

-- 表的索引 `event`
--

-- ALTER TABLE `event`
  -- ADD PRIMARY KEY (`event_id`);

-- --------------------------------------------------------

--
-- 表的结构 `coursebase`
--

CREATE TABLE `coursebase` (
  `c_code` varchar(20) NOT NULL,
  `c_title` varchar(100) NOT NULL,
  `message` varchar(160),
  `c_zoom_link` varchar(160)
);



-- 表的索引 `coursebase`
--

ALTER TABLE `coursebase`
  ADD PRIMARY KEY (`c_code`);
  
  -- --------------------------------------------------------
  
  --
-- 表的结构 `courset`
--

CREATE TABLE `courset` (
  `c_code` varchar(20) NOT NULL,
  `c_day` char(3) NOT NULL,
  `c_time_start` time NOT NULL,
  `c_time_end` time NOT NULL,
  `lecturer` varchar(40),
  `tutor` varchar(40)
);



-- 表的索引 `courset`
--

ALTER TABLE `courset`
  ADD PRIMARY KEY (`c_code`,`c_day`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`);
  
  -- --------------------------------------------------------

--
-- 表的结构 `enrolled`
--

CREATE TABLE `enrolled` (
  `student_id` bigint(10) NOT NULL,
  `c_code` varchar(20) NOT NULL
);



-- 表的索引 `enrolled`
--

ALTER TABLE `enrolled`
  ADD PRIMARY KEY (`c_code`,`student_id`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`),
  ADD FOREIGN KEY (`student_id`) REFERENCES student(`student_id`);
-- --------------------------------------------------------



--
-- 表的结构 `tutorialbase`
--

CREATE TABLE `tutorialbase` (
  `c_code` varchar(20) NOT NULL,
  `t_num` int NOT NULL,
  `t_date` date NOT NULL,
  `t_day` varchar(3) NOT NULL,
  `t_time_start` time,
  `t_time_end` time
);



-- 表的索引 `tutorialbase`
--

ALTER TABLE `tutorialbase`
  ADD PRIMARY KEY (`t_num`,`c_code`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`);

-- --------------------------------------------------------

--
-- 表的结构 `coursem`
--

CREATE TABLE `coursem` (
  `c_code` varchar(20) NOT NULL,
  `c_num` int NOT NULL,
  `c_date` date,
  `c_material_link` varchar(200)
);


-- 表的索引 `coursem`
--

ALTER TABLE `coursem`
  ADD PRIMARY KEY (`c_num`,`c_code`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`);
-- --------------------------------------------------------

--
-- 表的结构 `tutorialm`
--

CREATE TABLE `tutorialm` (
  `c_code` varchar(20) NOT NULL,
  `t_num` int NOT NULL,
  `t_date` date NOT NULL,
  `t_material_link` varchar(200)
);


-- 表的索引 `tutorialm`
--

ALTER TABLE `tutorialm`
  ADD PRIMARY KEY (`c_code`,`t_num`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`);

-- --------------------------------------------------------

--
-- 表的结构 `DDL`
--

CREATE TABLE `DDL` (
  `c_code` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `ddl_date` date,
  `ddl_time` time,
  `ddl_submit_link` varchar(200)
);


-- 表的索引 `DDL`
--

ALTER TABLE `DDL`
  ADD PRIMARY KEY (`name`,`c_code`),
  ADD FOREIGN KEY (`c_code`) REFERENCES coursebase(`c_code`);

-- --------------------------------------------------------

