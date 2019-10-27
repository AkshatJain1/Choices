import React, {Component} from 'react';
import {View, Text, StyleSheet, FlatList, Animated, TouchableOpacity, Button} from 'react-native';
import AsyncStorage from '@react-native-community/async-storage';

const AnimatedButton = Animated.createAnimatedComponent(TouchableOpacity)


export default class Dietary extends Component{

  constructor(props) {
    super(props);
    this.restr = ['Lactose Intolerance', 'Vegetarian', 'Peanut Allergies', 'Diabetic', 'Gluten Free'] // kosher halal
    this.restr = this.restr.map((item,i) => {
      return {
        id: i.toString(),
        title: item,
        checked: false,
        animated_value: new Animated.Value(0),
      }
    })
    this.state = {};

    this.onBubbleClick = this.onBubbleClick.bind(this);
    this.saveDietary = this.saveDietary.bind(this);
  }

  onBubbleClick = item_id => {
    element = this.restr.find(v => v.id == item_id)
    val = element.animated_value
    Animated.timing(val, {
       toValue: (val._value == 150 ? 0 : 150),
       duration: 800
    }).start();

     element.checked = !element.checked

  };

  saveDietary = async () => {
    // store in AsyncStorage
    try {
      await AsyncStorage.setItem('@dietary', JSON.stringify(this.restr.map(item => {
        return {
          title: item.title,
          checked: item.checked,
        }
      })))
    } catch (e) {
      // saving error
    }
    console.log('saving diet', this.restr.map(item => {
      return {
        title: item.title,
        checked: item.checked,
      }
    }));
    //navigate to dietary restrictions page
    this.props.navigation.navigate('Preferences');
  }

  render() {
    const interpolateColor = val => {
      return val.interpolate({
        inputRange: [0, 150],
        outputRange: ['rgb(255,255,0)', 'rgb(51, 250, 170)']
      })
    };

    const animatedStyle = val => {
      return {
        backgroundColor: interpolateColor(val),
      }
    };

    return (
      <View style = {styles.container}>
      <Text style={styles.title}>
            Preferences
      </Text>
        <FlatList
          data = {this.restr}
          contentContainerStyle={{flexGrow: 1, justifyContent: 'space-evenly'}}
          renderItem = {({ item }) => <AnimatedButton style = {[styles.bubble, animatedStyle(item.animated_value)]} onPress = {() => this.onBubbleClick(item.id)}><Text>{ item.title }</Text></AnimatedButton>}
          keyExtractor={item => item.id}
        />
        <TouchableOpacity
          style={styles.customBtnBG}
          onPress={this.saveDietary}  >
          <Text style={styles.customBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  customBtnText: {
    fontSize: 30,
    color: '#FFFF00',
    fontWeight: 'bold',
    alignItems:'center',
    justifyContent: 'center',
  },
  customBtnBG: {
    backgroundColor: '#33FAAA',
    paddingHorizontal: 15,
    paddingVertical: 2,
    
    borderRadius: 30,
    marginBottom: 40,
    alignItems:'center',
    justifyContent: 'center',
  },
  title: {
    marginTop: 70,
    color: '#33FAAA',
    fontWeight: 'bold',
    fontSize: 30,
    width:250,
    height:40,
    textAlign: 'center',
    alignItems:'center',
    justifyContent: 'center',
    marginBottom: 30,
},
  
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00b5ec',
  },
  bubble: {
      backgroundColor: '#FFFFFF',
      borderRadius:50,
      width:250,
      height:80,
      alignItems:'center',
      justifyContent: 'center',
  },
})
