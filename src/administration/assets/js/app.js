'use strict';

var app = angular.module('playAdmin', [
    'ngRoute',
    'playControllers'
]);


app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/index', {
            templateUrl: '/administration/dashboard',
            controller: 'EmptyCtrl'
        }).
        when('/courses', {
            templateUrl: '/administration/courses',
            controller: 'CoursesListCtrl'
        }).
        when('/courses/details/:id', {
            templateUrl: '/administration/courses/course_details',
            controller: 'CoursesCtrl'
        }).
        when('/teachers', {
            templateUrl: '/administration/courses/teacher_list',
            controller: 'TeachersListCtrl'
        }).
        when('/teachers/details/:id', {
            templateUrl: '/administration/courses/teacher_details',
            controller: 'TeachersCtrl'
        }).
        when('/course_add', {
            templateUrl: '/administration/courses/course_add',
            controller: 'CourseAddCtrl'
        }).
        when('/teacher_add', {
            templateUrl: '/administration/courses/teacher_add',
            controller: 'TeacherAddCtrl'
        }).
        when('/users', {
            templateUrl: '/administration/users',
            controller: 'usersCtrl'
        }).
        otherwise({
            redirectTo: '/index'
        });
    }
]);