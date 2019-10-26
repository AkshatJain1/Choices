import React, {Component} from 'react';
import {View, Text, StyleSheet} from 'react-native';
import AsyncStorage from '@react-native-community/async-storage';

export default class Scan extends Component{

  constructor(props) {
    super(props);

    this.state = {};
    this.clearAsyncStorage = this.clearAsyncStorage.bind(this)
  }

  clearAsyncStorage = async() => {
    AsyncStorage.clear();
  }

  render() {
    //temporary to test RegistrationStack
    this.clearAsyncStorage()
    return (
      <View style = {styles.container}>
        <Text>Hello you are in the scanning screen</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  }
})
