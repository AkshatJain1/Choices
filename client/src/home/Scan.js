import React, {Component} from 'react';
import {View, StyleSheet, Text} from 'react-native';

import Geolocation from 'react-native-geolocation-service';
import ImagePicker from 'react-native-image-picker';
import {PermissionsAndroid, Platform} from 'react-native';

const styles = StyleSheet.create({
    container: {
      ...StyleSheet.absoluteFillObject,
    }
});
  

export default class Scan extends Component {
    constructor(props) {
        super(props);

        this.state = {}

        if (Platform.OS === 'android') {
            this.requestLocationPermission();
        } else {
            this.getLocation()
            this.openCamera()
        }
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
            this.getLocation();
            this.openCamera();
          } else {
            console.log('Location permission denied');
          }
        } catch (err) {
          console.warn(err);
        }
    }

    getLocation = () => {
        Geolocation.getCurrentPosition(
            (position) => {
                this.setState({position})
                this.openCamera();
            },
            (error) => {
                console.log(error.code, error.message);
            },
            { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
        );
    }

    openCamera = () => {
        const options = {
            title: 'Select Menu Image',
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
                    console.log("uri" in response);
                }
            });
    }
    
    render() {
        return (
            <View>
                <Text>
                    Scan Screen
                </Text>
            </View>
        );
    }
}