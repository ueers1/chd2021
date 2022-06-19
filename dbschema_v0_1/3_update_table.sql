-- 完善student信息
ALTER TABLE student ADD college VARCHAR(64);
ALTER TABLE student ADD grade VARCHAR(64);
ALTER TABLE student ADD class VARCHAR(64);

-- 完善课程基础信息 
ALTER TABLE course ADD semester varchar(64); -- 学期
ALTER TABLE course ADD credits varchar(64); -- 学分
ALTER TABLE course ADD hours varchar(64); -- 学时

-- 创建课程表表结构
drop table if exists class_schedule;

create table class_schedule (
	id integer, -- 序号
	course_sn integer, -- 课程序号
    clas_shift integer, -- 班次 1
	class_location varchar(256), -- 地点
	class_date varchar(256), -- 时间
	class_teacher varchar(256), -- 任课教师
	primary key(id)
);

-- ALTER TABLE class_schedule ALTER COLUMN course_sn TYPE varchar(256);
ALTER TABLE class_schedule ALTER COLUMN class_date TYPE varchar(256);

-- 添加自增序列
CREATE SEQUENCE seq_class_schedule_id 
    START 1 INCREMENT 1 OWNED BY class_schedule.id;
ALTER TABLE class_schedule ALTER id
    SET DEFAULT nextval('seq_class_schedule_id');

-- 添加外键
ALTER TABLE class_schedule 
    ADD CONSTRAINT course_sn_fk FOREIGN KEY (course_sn) REFERENCES course(sn);

-- 添加unique key
-- 一个老师不能再同一时间有两节课
alter table class_schedule add constraint uk_teacher_date_shift unique (clas_shift,class_date,class_teacher);
-- 一个教室不能同一个时间有2节课
alter table class_schedule add constraint uk_location_date_shift unique (clas_shift,class_date,class_location);

-- 学生选课信息
create table student_course(
	id bigint,
	student_sn bigint,
	class_schedule_id bigint,
	primary key(id)
);

-- 添加自增序列
CREATE SEQUENCE seq_student_course_id 
    START 1 INCREMENT 1 OWNED BY student_course.id;
ALTER TABLE student_course ALTER id
    SET DEFAULT nextval('seq_student_course_id');

-- 添加外键
ALTER TABLE student_course
    ADD CONSTRAINT student_course_student_sn_fk FOREIGN KEY (student_sn) REFERENCES student(sn);
ALTER TABLE student_course
    ADD CONSTRAINT student_course_class_schedule_id_fk FOREIGN KEY (class_schedule_id) REFERENCES class_schedule(id);

-- 添加unique key，同一个学生不能选同一个课2次
alter table student_course add constraint uk_student_sn_class_schedule_id unique (student_sn,class_schedule_id);