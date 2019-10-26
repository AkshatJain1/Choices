import Scan from './Scan';
import AsyncStorage from '@react-native-community/async-storage';
import CreateAccount from './CreateAccount';
import Preferences from './Preferences';
import Dietary from './Dietary';
import React, {Component} from 'react';
import {View, StyleSheet, StatusBar} from 'react-native';
import { createAppContainer, createSwitchNavigator } from 'react-navigation';

const RegistrationStack = createSwitchNavigator({
  CreateAccount: CreateAccount,
  Dietary: Dietary,
  Preferences: Preferences,
})

const RegistrationContainer = createAppContainer(RegistrationStack, {
  initialRouteName: 'CreateAccount',
})

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {'logged_in' : false};
    this.loadInitialScreen = this.loadInitialScreen.bind(this);
    this.loadInitialScreen();
  }

  loadInitialScreen = async () => {
    try{
      const value = await AsyncStorage.getItem('@username')
      if(value !== null) {
        this.setState({'logged_in' : true})
      } else {
        this.setState({'logged_in' : false})
      }
    } catch (e) {
      this.setState({'logged_in' : false})
    }
  }

  render() {
    return(
        this.state.logged_in ? <View style = {styles.container}><StatusBar hidden /><Scan /></View> : <View style = {styles.container}><StatusBar hidden /><RegistrationContainer /></View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
  }
})
