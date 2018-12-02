-- Database setup file for baseball-app
create database baseball_app_db;

use baseball_app_db;

-- user table
create table user (
    id                  int             primary key,
    username            varchar(64)     not null unique,
    email               varchar(120)    not null unique,
    password_hash       varchar(120),
    about_me            varchar(140),
    last_seen           datetime,                                           -- yyyy-mm-dd hh:mm:ss
    image_path          varchar(120),
    first_name          varchar(120),
    last_name           varchar(120),
    full_name           varchar(140)
);

-- fanasy table
create table fantasy (
    id                  int             primary key,
    user_id             int             references user(id),
    team_name           varchar(120),
    image_path          varchar(120),
    city                varchar(120),
    state               varchar(120),
    mascot              varchar(120),
    field_name          varchar(120),
    conference_id       int             references conference(id)
);

-- conference table
create table conference (
    id int primary key,
    name varchar(120),
    -- universities     using a query to acquire the list of universities
    image_path varchar(120)
);

-- university table
create table university (
    id                  int            primary key,
    name                varchar(120),
    mascot              varchar(120),
    city                varchar(120),
    state               varchar(120),
    field_name          varchar(120),
    -- athletes         using a query to acquire the list of athletes
    -- staff            using a query to acquire teh list of staff
    conference_id       int            references conference(id),
    image_path          varchar(120)
);

-- athlete table
create table athlete (
    id                  int            primary key,
    first_name          varchar(120)   not null,
    last_name           varchar(120)   not null,
    DOB                 varchar(11)    not null,                            -- in format mm/dd/yyyy
    enrollment_data     varchar(11),                                        -- in format mm/dd/yyyy
    scholarship_amount  decimal(8,2),
    country_of_origin   varchar(120),
    university_id       int            references unversity(id),
    fantasy_id          int            references fantasy(id),
    image_path          varchar(120),
    weight              decimal(5,2),                                       -- this is all in pounds (187.56 pounds)
    height              varchar(20),                                        -- what is the formatting for this?
    bats                enum('L', 'R', 'S'),                                -- left, right, switch
    throws              enum('L', 'R', 'S'),                                -- left, right, switch
    position            enum('P', 'C', 'INF', 'OF'),                        -- pitcher, catcher, infield, outfield
    number              int,
    high_school         varchar(120)
);

-- staff table
create table staff (
    id                  int            primary key,
    first_name          varchar(120)   not null,
    last_name           varchar(120)   not null,
    DOB                 varchar(11)    not null,                            -- in format mm/dd/yyyy
    start_date          varchar(11),                                        -- in format mm/dd/yyyy
    job_title           varchar(120),
    university_id       int            references unversity(id),
    image_path          varchar(120)
);

-- pitcher career table
create table pitcher_career (
    athlete_id          int             references athlete(id),
    appearances         int,
    innings_thrown      int,
    runs_allowed        int,
    earned_run_average  int,
    strikeouts          int
);

-- postion player career table
create table position_player_career (
    athlete_id          int             references athlete(id),
    games_played        int,
    innings_played      int,
    at_bats             int,
    hits                int,
    walks               int,
    runs_scored         int,
    runs_batted_in      int,
    home_runs           int,
    batting_average     decimal(4,3)
);