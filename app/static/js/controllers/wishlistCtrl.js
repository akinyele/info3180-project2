

app.controller('wishlistController',function($rootScope,$scope,$http,$location,base_url) {
    
    //$scope.user = {}
    //$scope.wishlist = []
    $scope.message = ""
    
    
    //TO DO: add $scope watches for certain varialbs 
    

    let token = "";
    $scope.welcome = "Welcome to our wish list :) ";
    
    if( localStorage.getItem('isLogin') == 'true' ){
        $scope.loginText = 'Logout';
    }else{
         $scope.loginText = 'Login';
    }
    
    
    
                       
                        
    $scope.register = function(event){
        
        event.preventDefault();
        
        //Recieving token
        $http.post(base_url+"/token",
        {
          password: $scope.password,
          email: $scope.email
        },
        {
            'headers': {
            'Content-Type': 'application/json',
            // 'Authorization': 'Basic ' + localStorage.getItem('token')
            }
            
        }).then(function(response){
            
            let token = response.data;
            localStorage.setItem('token', token);
            
            console.info('Token generated and added to localStorage. <' + token +'>');
            $scope.token = token;
        
            var req = {
            
                method:'POST',
                url:base_url + '/api/users/register',
                headers : {
                    'Content-Type':'application/json',
                    'Authorization': 'Basic '+ token
                
                },
                data : {
                    email: $scope.email,
                    name: $scope.name,
                    password: $scope.password,
                    age: $scope.age,
                    gender: $scope.gender,
                    image: $scope.image
                }
            };
            
            $http(req).then(function(response){
                
                console.info('user registered');
                console.info('user:'+ $scope.name +
                             ' gender:  ' + $scope.gender +
                             ' age: ' + $scope.age +
                             ' image:' + $scope.image +
                             ' token: ' + localStorage.getItem('token') );
                
                $location.path('/');
                
            },function(response) {
                  $scope.data = response.data || 'Request failed';
                  $scope.status = response.status;
            });
        });
        
    };//end of registration function
    
    $scope.user_login= function(event){
        //$scope.wishlist = [];
        
        //Recieving token
        $http.post(base_url+"/token",{
          password: $scope.password,
          email: $scope.email
        },
        {
            'headers': {
            'Content-Type': 'application/json',
            //'Authorization': 'Basic ' + localStorage.getItem('token')
        }})
        
        .then( function(response){ // after token reciever mmakes request to API
            
            //store token
            token = response.data;
            localStorage.setItem('token', token);
            
            console.info('Token generated and added to localStorage.<' + token +'>');
            
            //making request to be sent ot server
            var req = {
                method: 'POST',
                url: base_url+'/api/users/login',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic '+ localStorage.getItem('token')
                },
                data: { email: $scope.email, password: $scope.password }
            }
        
            //sending login request
            $http(req).then( function(response){
                    
                    //TODO: on successfull login set user login state to true
                    let message = response.message;
                    console.log(" error:" +response.data.error)
                    console.log(" message:" +response.data.message)
                    console.log(" id:" +response.data.data['user']['id'])
                    
                    
                    //$scope.wishlist.push('item')
                    // if there was no error send to user to wish list his wishlist route.    
                    if( !response.data.error ){
                        localStorage.setItem("isLogin", true );
                        $scope.loginText='Logout';
                        
                        localStorage.setItem('cur_user', JSON.stringify(response.data.data['user']))
                        
                        
                        let user = JSON.parse(localStorage.getItem('cur_user'));
                        
                        console.log("local storage cur_user: "+user['id'] );
                        
                        var req = {
                            method: 'GET',
                            url: base_url+'/api/users/'+user['id']+'/wishlist',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Basic '+ localStorage.getItem('token')
                            },
                            data: {}
                        }
                        
                        $http(req).then(function(response) {
                            
                            if(response.data.error){
                                
                                $scope.error = response.data.error;
                                //$scope.wishlist = {}
                                $scope.message = response.data.message;
                                $rootScope.wishlist = []
                                console.log(response.data.message)
                                console.log('NO WISHLIST | '+ response.data.error )
                                
                            }else{
                                $scope.error = response.data.error;
                                $scope.message = response.data.message;
                                //$scope.wishlist.push(response.data.data['items'])
                                $rootScope.wishlist = []
                                for(i in response.data.data['items']){
                                    $rootScope.wishlist.push( response.data.data['items'][i] )
                                }
                                console.log(response.data.message)
                                console.log("root scope: " + $rootScope.wishlist)
                                
                            }
                        })
                        
                        $location.path('/wishlist');
                    }
                    
                  
                }
              
                
            );
        });
    };  //end of login function
    
    
    $scope.getUrl= function(event){ //access the API url scapper function
        event.preventDefault();
        
        
        
        
            
        //CANNOT SEND JSON DATA WITH GET REQUEST    
        var req = {
                 method: 'POST',
                 url:base_url+'/api/thumbnails',
                 headers: {
                   'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + localStorage.getItem('token')
                 },
                 data: {  url : $scope.wish_url }
                }
         
        
        $http(req).then(function(response) {
            
            if(response.data.error){
                console.log(response.data.message);
            }else{
                console.log(response.data.message);
                $scope.thumbnails = response.data.data['thumbnails']
            }
            
            
            
            
        });
        
    };//end of get url function
    
    
    
    $scope.addItem = function(event,index){
      
      event.preventDefault();
      
      console.log("title:"+$scope.item_title)
      console.log('desc: '+ $scope.item_desc)
      console.log('thumbnail_url', $scope.thumbnails[index] )
        
        
      var user = JSON.parse(localStorage.getItem('cur_user'))
      
      var req = {
          method:'POST',
          url:base_url+'/api/users/'+user['id']+'/wishlist',
          headers: {
                   'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + localStorage.getItem('token')
          },
          data: {  
            title : $scope.item_title,
            description:$scope.item_desc,
            url: $scope.wish_url,
            thumbnail_url:$scope.thumbnails[index]
              
          }
        }
        
        
        $http(req).then(function(response) {
            
            
            console.log("error: "+response.data.error)
            if(response.data.error){
                
            }else{
                console.log(response.data)
                $rootScope.wishlist.push(response.data.item)
            
                
                $location.path('wishlist')
            }
            
        });
              
      
      
      
      
        
    };
    
    
    
    $scope.get_wishes = function(event){
        event.preventDefault();
        
        var user = JSON.parse(localStorage.getItem('cur_user'));
        
        var req = {
            method: 'GET',
            url: base_url+'/api/users/'+ user['id']+'/wishlist',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic '+ localStorage.getItem('token')
            },
            data: {}
        }
        
        console.log("user id: " + user['id'])
        
        
        $http(req).then(function(response) {
            
            if(response.data.error){
                
                $scope.error = response.data.error;
                $scope.message = response.data.message;
                $rootScope.wishlist = []
                console.log(response.data.message)
                console.log('NO WISHLIST | ')
                
            }else{
                
                $scope.error = response.data.error;
                $scope.message = response.data.message;
                $rootScope.wishlist = []
                for(i in response.data.data['items']){
                    $rootScope.wishlist.push( response.data.data['items'][i] )
                }
                
                console.log(response.data.message)
                console.log("view_wishes root scope: " + $rootScope.wishlist)
                
            }
        })
        
    }
    
    
    
    $scope.delete = function(event,index){
        event.preventDefault();
        
        let delete_item = $rootScope.wishlist[index];
        
        var user = JSON.parse(localStorage.getItem('cur_user'));
        
        console.log("item id : " + delete_item.id)
        console.log("item url: " + delete_item.url)
        console.log("user id: " + user['id'])
        
        $rootScope.wishlist.splice(index,1)
        
        var req = {
            method:'DELETE',
            url:base_url+'/api/users/'+user['id']+'/wishlist/'+delete_item.id,
            headers:{
                'Content-Type': 'application/json',
                'Authorization': 'Basic '+ localStorage.getItem('token')
            },
            data:{
                id:delete_item.id
            }
        }
        
        
        $http(req).then(function(response) {
            
            console.log(response.data.message);
            
        })
        
        
    }
    
    
    console.log(localStorage.getItem('isLogin'));
   
   
    $scope.login_logout = function(event){
        event.preventDefault();
        
        
        if( localStorage.getItem('isLogin')=='true' ){ //if user is logge in then log them out and send them to the login page
        
            //TODO: logs out the user and clears local storage of vallues
            
            $scope.loginText = 'Login';
            localStorage.setItem('isLogin', false)
            localStorage.setItem('token', null)
            
            $location.path('/login');
            
        }else{  
            //if the user is not logged in it sends them to the login page...
            //come to think of it that should be the only page they should 
            //be able to acceess if not loged in 
        
             $scope.loginText = 'Login';
             $location.path('/login');
        }
        
        
    };    







});//end of controller




app.controller('login_reg_ctrl', function($scope,$http,$location,base_url){
    
    $scope.all_users = []
    $scope.wishlist = []
    
    
    
    $scope.LoginText = 'Login';
    
    
    
    
    
    
    
    
    
})





