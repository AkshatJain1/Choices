import React, {Component} from 'react';
import {View, Text, StyleSheet, Image, ActivityIndicator} from 'react-native';
import AsyncStorage from '@react-native-community/async-storage';
import ImagePicker from 'react-native-image-picker';
import {googleAPIKey as googleKey} from './app.json';
import Geolocation from 'react-native-geolocation-service';
import {PermissionsAndroid, Platform} from 'react-native';



export default class Scan extends Component{

  constructor(props) {
    super(props);

    this.state = {};
    // this.clearAsyncStorage = this.clearAsyncStorage.bind(this);
    this.requestLocationPermission = this.requestLocationPermission.bind(this);
    this.getLocation = this.getLocation.bind(this);
    this.openCamera = this.openCamera.bind(this);
    this.getRestaurant = this.getRestaurant.bind(this);
    if (Platform.OS === 'android') {
      this.requestLocationPermission();
    }
    else {
      this.getLocation()
      this.openCamera()
    }
    this.aggregateRestaurantReviews = this.aggregateRestaurantReviews.bind(this);

  }

  getLocation = () => {
    // Instead of navigator.geolocation, just use Geolocation.
    Geolocation.getCurrentPosition(
        (position) => {
            this.setState({position})
            this.getRestaurant();
        },
        (error) => {
            // See error code charts below.
            console.log(error.code, error.message);
        },
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
    );
  }

  openCamera = () => {
    // More info on all the options is below in the API Reference... just some common use cases shown here
    const options = {
      title: 'Select Avatar',
      customButtons: [{ name: 'fb', title: 'Choose Photo from Facebook' }],
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    // Launch Camera:
    ImagePicker.launchCamera(options, (response) => {
       if (response.didCancel) {
         console.log('User cancelled image picker');
       } else if (response.error) {
         console.log('ImagePicker Error: ', response.error);
       } else if (response.customButton) {
         console.log('User tapped custom button: ', response.customButton);
       } else {
         // const source = { uri: response.uri };
         console.log('querying menu parser');
         console.log(response.uri);
         console.log(Object.keys(response));
         // var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
         // encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t}}
         const createFormData = (photo, body) => {
           const data = new FormData();

           data.append("photo", {
             name: photo.fileName,
             type: photo.type,
             uri: Platform.OS === "android" ? photo.uri : photo.uri.replace("file://", "")
           });

           Object.keys(body).forEach(key => {
             data.append(key, body[key]);
           });

           return data;
         };

         // You can also display the image using data:
         const source = { uri: 'data:image/jpeg;base64,' + response.data };

         // fetch('https://choices2.appspot.com/', {
         //    method: 'GET',
         //  })
         //  .then(response => response.json())
         //  .then(response => {
         //    console.log("upload succes", response);
         //    alert("Upload success!");
         //    this.setState({ photo: null });
         //  })
         //  .catch(error => {
         //    console.log("upload error", error);
         //    alert("Upload failed!");
         //  });

         fetch('http://10.142.126.32:5000/', {
            method: 'POST',
            body: JSON.stringify({'data': response.data}),
            headers: {"Content-Type": "application/json"}
          })
          .then(response => response.json())
          .then(response => {
            console.log("upload succes", response);
            alert("Upload success!");
            this.setState({ photo: null });
          })
          .catch(error => {
            console.log("upload error", error);
            alert("Upload failed!");
          });


         this.setState({
           avatarSource: source,
         });
       }
    });
  }

 requestLocationPermission = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'Cool Photo App Location Permission',
          message:
            'Cool Photo App needs access to your location ' +
            'so you can get better recommendations.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        this.getLocation()
        this.openCamera()
      } else {
        console.log('Location permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  }

  getRestaurant = () => {
    fetch(`https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&location=${this.state.position.coords.latitude},${this.state.position.coords.longitude}&radius=5&key=${googleKey}`)
      .then(response => response.json())
      .then(response => {
          this.setState({restaurantGoogleId: response.results[0].place_id ,restaurantName: response.results[0].name, restaurantAddress: response.results[0].formatted_address})
          console.log(this.state.restaurantGoogleId, this.state.restaurantName, this.state.restaurantAddress);
          this.aggregateRestaurantReviews();
      })
      .catch(error => console.error(error))
  }

  aggregateRestaurantReviews = () => {
    totalReviews = []
    //google reviews
    fetch(`https://maps.googleapis.com/maps/api/place/details/json?place_id=${this.state.restaurantGoogleId}&key=${googleKey}`)
      .then(response => response.json())
      .then(response => {
        google_reviews = response.result.reviews;
        google_reviews.forEach(review => totalReviews.push(review.text))
        this.setState({totalReviews})

      })
      .catch(error => console.error(error))
  }

  // popularItems = () => {
  //   const client = new language.LanguageServiceClient();
  //   top5 = []
  //   countForItem = len(reviews) * [[]]
  //   reviews = this.state.totalReviews //list of strings
  //   menuItems = [['a', 5.0], ['b', 2.0], ['c', 2.5], ['d', 6.5], ['e', 1.0], ['f', 7.7]]// list [[menu_item_name, price] ... ]
  //   this.state.totalReviews.forEach( review => {
  //     fetch(`https://language.googleapis.com/v1beta2/documents:documents:analyzeEntitySentiment?document=${{}}&key=${googleKey}`)
  //       .then(response => response.json())
  //       .then(response => {
  //
  //       })
  //   })
  //
  //     //return the top 5 popular menu items based on reviews (how many times the item was mentioned in the review)
  // }





  render() {
    //temporary to test RegistrationStack
    // clearAsyncStorage = async() => {
    //   AsyncStorage.clear();
    // }
    // this.clearAsyncStorage()

    return (
      <View style = {styles.container}>
        <ActivityIndicator size="small" color="#00ff00" />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  uploadAvatar: {
    width: 400,
    height: 600,
    justifyContent: 'center',
    resizeMode: 'contain'
  }
})
