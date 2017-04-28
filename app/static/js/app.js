/* Add your Application JavaScript */


var app = angular.module('wishlistApp', ["ngRoute"]);

//let base_url = "http://info3180-project2-akinyele.c9users.io:8080";

app.value('base_url', 'http://info3180-project2-akinyele.c9users.io:8080');


app.factory('getToken', function(){
    
});


app.config(function($routeProvider,$locationProvider){
    $routeProvider
    .when('/',  {
        templateUrl: "/static/partials/index.html",
        controller: "wishlistController"
        
    })
    .when('/login', {
        templateUrl:'/static/partials/login.html',
        controller: 'wishlistController'
    })
    .when('/about',{
        templateUrl:'/static/partials/about.html',
        controller: 'wishlistController'
    })
    .when('/logout',{
        templateUrl:'/static/partials/login.html',
        controller: 'wishlistController'
        
    })
    .when('/wishlist',{
        templateUrl:'/static/partials/wishlist.html',
        controller: 'wishlistController'
        
    })
    .when('/addwish',{
        templateUrl:'/static/partials/addwish.html',
        controller:'wishlistController'
    })
    // .when('',{
    //     templateUrl:'/static/partials/'
    // })
    .otherwise({
        redirect:'/'
    });

    $locationProvider.html5Mode(true);
});


app.run(function($rootScope) {
    $rootScope.wishlist = [];
});

