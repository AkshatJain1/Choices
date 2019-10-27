import React, { Component } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  TouchableHighlight,
  Image,
  Alert
} from 'react-native';
import AsyncStorage from '@react-native-community/async-storage';


export default class CreateAccount extends Component {

  constructor(props) {
    super(props);
    this.state = {
      fullName: '',
      email   : '',
      password: '',
    }

    this.onClickListener = this.onClickListener.bind(this);
  }

  onClickListener = async () => {
    // store in AsyncStorage
    try {
      await AsyncStorage.setItem('@username', this.state.fullName)
      console.log('setting item');
    } catch (e) {
      // saving error
      console.error(e);
    }
    //navigate to dietary restrictions page
    this.props.navigation.navigate('Dietary');
  }

  render() {
    return (
      <View style={styles.container}>

        <Image style={styles.contain} source={{uri: 'https://i.imgur.com/HX6pJYu.png'}}/>
        <View style={styles.inputContainer}>
          <Image style={styles.inputIcon} source={{uri: 'https://png.icons8.com/male-user/ultraviolet/50/3498db'}}/>
          <TextInput style={styles.inputs}
              placeholder="Full name"
              required
              keyboardType="email-address"
              underlineColorAndroid='transparent'
              onChangeText={(fullName) => this.setState({fullName})}/>
        </View>

        <View style={styles.inputContainer}>
          <Image style={styles.inputIcon} source={{uri: 'https://img.icons8.com/ultraviolet/48/000000/email.png'}}/>
          <TextInput style={styles.inputs}
              placeholder="Email"
              keyboardType="email-address"
              underlineColorAndroid='transparent'
              onChangeText={(email) => this.setState({email})}/>
        </View>

        <View style={styles.inputContainer}>
          <Image style={styles.inputIcon} source={{uri: 'https://png.icons8.com/key-2/ultraviolet/50/3498db'}}/>
          <TextInput style={styles.inputs}
              placeholder="Password"
              secureTextEntry={true}
              underlineColorAndroid='transparent'
              onChangeText={(password) => this.setState({password})}/>
        </View>

        <TouchableHighlight style={[styles.buttonContainer, styles.signupButton]} onPress={this.onClickListener}>
          <Text style={styles.signUpText}>Sign up</Text>
        </TouchableHighlight>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#00b5ec',
  },
  contain: {
    width: 250,
    height: 175,
    justifyContent: 'center',
    resizeMode: 'contain'
  },
  inputContainer: {
      borderBottomColor: '#F5FCFF',
      backgroundColor: '#FFFFFF',
      borderRadius:30,
      borderBottomWidth: 1,
      width:250,
      height:45,
      marginBottom:20,
      flexDirection: 'row',
      alignItems:'center'
  },
  inputs:{
      height:45,
      marginLeft:16,
      borderBottomColor: '#FFFFFF',
      flex:1,
  },
  inputIcon:{
    width:30,
    height:30,
    marginLeft:15,
    justifyContent: 'center'
  },
  buttonContainer: {
    height:45,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom:20,
    width:250,
    borderRadius:30,
  },
  signupButton: {
    backgroundColor: "#e45f1c",
  },
  signUpText: {
    color: 'white',
  }
});
