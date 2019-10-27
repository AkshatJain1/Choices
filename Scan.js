import React, {Component} from 'react';
import {View, Text, StyleSheet, Image} from 'react-native';
import AsyncStorage from '@react-native-community/async-storage';
import ImagePicker from 'react-native-image-picker';


export default class Scan extends Component{

  constructor(props) {
    super(props);

    this.state = {};
    this.clearAsyncStorage = this.clearAsyncStorage.bind(this)

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
      console.log('Response = ', response);

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

  clearAsyncStorage = async() => {
    AsyncStorage.clear();
  }

  render() {
    //temporary to test RegistrationStack
    // this.clearAsyncStorage()

    return (
      <View style = {styles.container}>
        <Image source={this.state.avatarSource} style={styles.uploadAvatar} />
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
