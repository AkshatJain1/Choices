import React, {Component} from 'react';
import {View, StyleSheet, StatusBar, AsyncStorage} from 'react-native';
import { createAppContainer, createSwitchNavigator } from 'react-navigation';
// import AsyncStorage from '@react-native-community/async-storage';

import * as eva from '@eva-design/eva';
import { ApplicationProvider, Layout, Text } from '@ui-kitten/components';


/*
  Import Components
*/
import Welcome from './welcome';
import Preferences from './welcome/Preferences';
import Demographic from './welcome/Demographic';
import Scan from './home/Scan';

const RegistrationStack = createSwitchNavigator({
  Welcome: Welcome,
  Demographic: Demographic,
  Preferences: Preferences,
  Scan: Scan,
})



class App extends Component {
  constructor(props) {
    super(props);

    // Assume not logged in
    this.state = {initialRoute : 'Welcome'};

    // set state's initialRoute appropriately
    this.loadInitialScreen();
  }

  loadInitialScreen = async () => {
    try{
      const value = await AsyncStorage.getItem('@id')
      if(value !== null) {
        this.setState({initialRoute : 'Scan'})
      }
    } catch (e) {
        console.log(e);
    }
  }

  render() {
    const RegistrationContainer = createAppContainer(RegistrationStack, {
      initialRouteName: this.state.initialRoute,
    })
    return( 
      <Layout style={[styles.container, {flex: 1, justifyContent: 'center', alignItems: 'center'}]}>
        <StatusBar hidden />
        <RegistrationContainer />
      </Layout>
    );
  }
}

export default () => (
  <ApplicationProvider {...eva} theme={eva.light}>
    <App />
  </ApplicationProvider>
);

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
  }
})
