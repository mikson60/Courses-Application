'use strict';

var playControllers = angular.module('playControllers', [
    'ui.bootstrap',
    'ngTable',
    'ngResource',
    'kitAdminServices'
]);



playControllers.controller('EmptyCtrl', ['$scope', function ($scope) {
}]);


playControllers.controller('CoursesListCtrl',
    ['$scope', '$http', 'ngTableParams', 'CourseServ',
    function ($scope, $http, ngTableParams, CourseServ) {


        $scope.tableParams = new ngTableParams({
                page: 1,
                count: 10,
            }, {
                total: 0,
                getData: function($defer, params) {
                    CourseServ.list(params.url(), function(resp) {
                        params.total(resp.total);
                        $scope.data = resp.rows;
                        $scope.teachers = resp.teachers;
                        console.log($scope.data["26"]);
                        $defer.resolve($scope.data);
                        $defer.resolve($scope.teachers);
                    });
                }
            });

        $scope.removeCourse = function(course_id) {
            CourseServ.delete({id: course_id}, function(resp) {
                console.log($scope.data);
                delete $scope.data[course_id.toString()];
            });
        };

        $scope.addTeacher = function(course, teacher) {
            CourseServ.editTeacher({ course_id: course,
                         teacher_id:teacher, action:"assignTeacher"
                      }, function(resp) {
                $scope.data[course].teachers[teacher] = resp.teacher;
            });
        };

        $scope.remTeacher = function(course, teacher) {
          CourseServ.editTeacher({ course_id: course,
                       teacher_id:teacher, action:"removeTeacher"
                    }, function(resp) {
                    delete $scope.data[course].teachers[teacher];
          });
    };

    }]
);

playControllers.controller('CoursesCtrl',
    ['$scope', '$routeParams', 'CourseServ',
    function ($scope, $routeParams, CourseServ) {
        CourseServ.get($routeParams, function(resp) {
        	console.log($routeParams);
            $scope.course = resp.course
        });
    }]
);

playControllers.controller('TeachersListCtrl',
    ['$scope', 'ngTableParams', 'TeacherServ',
    function ($scope, ngTableParams, TeacherServ) {


        $scope.tableParams = new ngTableParams({
                page: 1,
                count: 10,
            }, {
                total: 0,
                getData: function($defer, params) {
                    TeacherServ.list(params.url(), function(resp) {
                        params.total(resp.total);
                        $scope.data = resp.rows;
                        console.log($scope.data[0])
                        $defer.resolve(resp.rows);
                    });
                }
            });

        $scope.removeTeacher = function(teacher_id) {
            TeacherServ.delete({id: teacher_id}, function(resp) {
                console.log($scope.data);
                for(var i=0; i < $scope.data.length; i++) {
                    if ($scope.data[i].id == teacher_id) {
                        $scope.data.splice(i, 1);
                        break;
                    }
                }

            });
        };
    }]
);

playControllers.controller('TeachersCtrl',
    ['$scope', '$routeParams', 'TeacherServ',
    function ($scope, $routeParams, TeacherServ) {
        TeacherServ.get($routeParams, function(resp) {
            $scope.teacher = resp.teacher;
            console.log(resp)
        });
    }]
);

playControllers.controller('CourseAddCtrl',
    ['$scope', '$routeParams', 'CourseAdd',
    function ($scope, $routeParams, CourseAdd) {

      $scope.submitCourse = function(name, code, capacity) {
          console.log('Name is: '+name);
          console.log('Code is: '+code);
          console.log('Capacity is: '+parseInt(capacity));
          CourseAdd.addCourse({ course_name: name,
                       course_code: code, course_capacity: parseInt(capacity)
                    }, function(resp) {
          });
      };

    }]
);

playControllers.controller('TeacherAddCtrl',
    ['$scope', '$routeParams', 'TeacherAdd',
    function ($scope, $routeParams, TeacherAdd) {

      $scope.submitTeacher = function(first_name, last_name) {
          console.log('First Name is: '+first_name);
          console.log('Last name is: '+last_name);
          TeacherAdd.addTeacher({ t_first_name: first_name,
                       t_last_name: last_name}, function(resp) {
          });
      };

    }]
);


playControllers.controller('usersCtrl', ['$scope', '$http', function ($scope, $http) {
    $http.get('/administration/users/list').success(function(data) {
        $scope.users = data.users;
        $scope.all_roles = data.all_roles;
    }).error(function(err) {
        return(err);
    });

    $scope.addRole = function(user, role) {
        $http.get('/administration/users/action', {
                method: "GET",
                params: {
                    action:"addRole",
                    user_id:user,
                    role_id:role
                    }
                })
            .success(function(resp) {
                $scope.users[user].roles[role] = resp.role;
            });
    };

    $scope.remRole = function(user, role) {
        $http.get('/administration/users/action', {
                method: "GET",
                params: {
                    action:"remRole",
                    user_id:user,
                    role_id:role
                    }
                })
            .success(function(resp) {
                delete $scope.users[user].roles[role];
            });
    };
}]);
