import React, {Component} from 'react';
import {View, StyleSheet, Text} from 'react-native';

const styles = StyleSheet.create({
    container: {
      ...StyleSheet.absoluteFillObject,
    }
});
  

export default class Dietary extends Component {
    constructor(props) {
        super(props);
        
    }
    
    render() {
        return (
            <View>
                <Text>
                    Dietary Screen
                </Text>
            </View>
        );
    }
}