/* Add your Application JavaScript */


var app = angular.module('wishlistApp', ["ngRoute"]);


app.value('base_url', 'http://info3180-project2-akinyele.c9users.io:8080');

app.value('api_url', 'https://whispering-eyrie-16954.herokuapp.com');





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


app.run(function($rootScope,$location) {
   
   
   $rootScope.wishlist = [];
    
    
    $rootScope.$on('$routeChangeStart', function (event,next) {
        
        var route = next.$$route.templateUrl
        
        if(route.includes('about.html')){
            console.log('ALLOW');
        }else if ( localStorage.getItem('token')==null ) {
            console.log('DENY');
            //event.preventDefault();
            $location.path('/login');
        }
        else {
            console.log('ALLOW');
            //$location.path('/home');
        }
        
    });
    
    
    
});

