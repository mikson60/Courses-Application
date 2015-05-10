var playServices = angular.module('kitAdminServices', ['ngResource']);

playServices.factory('CourseServ',
    ['$resource',
    function($resource){
        return $resource('/administration/courses/course', {}, {
            list: {method:'GET', params:{}, isArray:false, url:'/administration/courses/course/list'}
        });
    }]
);

playServices.factory('TeacherServ',
    ['$resource',
    function($resource){
        return $resource('/administration/courses/teacher', {}, {
            list: {method:'GET', params:{}, isArray:false, url:'/administration/courses/teacher/list'}
        });
    }]
);

playServices.factory('CourseAdd', 
    ['$resource',
    function($resource){
        return $resource('administration/courses/course/add', {}, {
        });
    }]
);

playServices.factory('TeacherAdd', 
    ['$resource',
    function($resource){
        return $resource('administration/courses/teacher/add', {}, {
        });
    }]
);