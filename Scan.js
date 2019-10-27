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
      this.requestLocationPermission()
    }
    else {
      this.getLocation()
      this.openCamera()
    }
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
         const source = { uri: response.uri };

         // You can also display the image using data:
         // const source = { uri: 'data:image/jpeg;base64,' + response.data };

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

  getRestaurant = () =>{
    fetch(`https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&location=${this.state.position.coords.latitude},${this.state.position.coords.longitude}&radius=5&key=${googleKey}`)
      .then(response => response.json())
      .then(response => {
          this.setState({restaurantName: response.results[0].name, restaurantAddress: response.results[0].formatted_address})
          console.log(this.state.restaurantName, this.state.restaurantAddress);
      })
      .catch(error => console.error(error))
  }





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
