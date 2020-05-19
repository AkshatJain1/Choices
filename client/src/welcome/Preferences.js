import React, {Component} from 'react';
import {View, StyleSheet, Text} from 'react-native';

const styles = StyleSheet.create({
    container: {
      ...StyleSheet.absoluteFillObject,
    }
});
  

export default class Preferences extends Component {
    constructor(props) {
        super(props);
        
    }
    
    render() {
        return (
            <View>
                <Text>
                    Preferences Screen
                </Text>
            </View>
        );
    }
}