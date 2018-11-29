-- Database setup file for baseball-app

-- user table
create table user(
    id                  number(4,0) primary key,
    username            varchar2(64) not null unique,
    email               varchar2(120) not null unique,
    password_hash       varchar2(120),
    about_me            varchar2(140),
    last_seen           datetime,                                           -- yyyy-mm-dd hh:mm:ss
    image_path          varchar2(120),
    first_name          varchar2(120),
    last_name           varchar2(120),
    full_name           varchar2(140)
);

-- athlete table
create table athlete (
    first_name          varchar2(120)   primary key,
    last_name           varchar2(120)   primary key,
    DOB                 varchar2(11)    primary key,                        -- in format mm/dd/yyyy
    enrollment_data     varchar2(11),                                       -- in format mm/dd/yyyy
    scholarship_amount  number(8,2),
    country_of_origin   varchar2(120),
    university_id       number(4,0)     references unversity(id),
    image_path          varchar2(120),
    weight              number(5,2),
    height              varchar2(20),                                       -- what is the formatting for this?
    bats                enum('L', 'R', 'S'),                                -- left, right, switch
    throws              enum('L', 'R', 'S'),                                -- left, right, switch
    position            enum('P', 'C', 'INF', 'OF'),                        -- pitcher, catcher, infield, outfield
    number              number(2,0),
    high_school         varchar2(120)
);

-- university table
create table unversity (
    id                  number(4,0)     primary key,
    name                varchar2(120),
    mascot              varchar2(120),
    city                varchar2(120),
    state               varchar2(120),
    field_name          varchar2(120),
    -- athletes         need to collect list of athletes
    -- staff            need to collect list of staff
    conference_id       number(4,0)     references conference(id),
    image_path          varchar2(120)
);

-- staff table
create table staff (
    first_name          varchar2(120)   primary key,
    last_name           varchar2(120)   primary key,
    DOB                 varchar2(11)    primary key,                        -- in format mm/dd/yyyy
    start_date          varchar2(11),                                       -- in format mm/dd/yyyy
    job_title           varchar2(120),
    university_id       number(4,0)     references unversity(id),
    image_path          varchar2(120)
);

-- conference table
create table conference (
    id                  number(4,0)     primary key,
    name                varchar2(120),
    -- universities     need list of universities
    image_path          varchar2(120)
);