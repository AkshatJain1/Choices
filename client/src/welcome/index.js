import React, {Component} from 'react';
import {View, StyleSheet, ImageBackground, Animated} from 'react-native';
import { Text } from '@ui-kitten/components';


const styles = StyleSheet.create({
    container: {
        ...StyleSheet.absoluteFillObject,
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#00b5ec',
    },
    image: {
        alignItems: 'center',
        justifyContent: "flex-end",
    },
});
  
  

export default class Welcome extends Component {

    state = {
        fadeAnim: new Animated.Value(0),
        show: new Animated.Value(0),
        topImage: new Animated.Value(5.5),
        botImage: new Animated.Value(5.5)
    }

    constructor(props) {
        super(props);
        this.fadeIn();

        Animated.timing(this.state.topImage, {
            toValue: 3,
            duration: 2000
        }).start();
        Animated.timing(this.state.botImage, {
            toValue: 8,
            duration: 2000
        }).start(this.textFadeIn);
    }

    textFadeIn = () => {
        Animated.timing(this.state.show, {
            toValue: 1,
            duration: 800
        }).start();
    }

    fadeIn = () => {
        // Will change fadeAnim value to 1 in 5 seconds
        Animated.timing(this.state.fadeAnim, {
          toValue: 1,
          duration: 1000
        }).start(this.fadeOut);
    };

    fadeOut = () => {
        // Will change fadeAnim value to 0 in 5 seconds
        Animated.timing(this.state.fadeAnim, {
            toValue: 0,
            duration: 1000
        }).start(this.fadeIn);
    };    
    
    render() {
        return (
            <View style={styles.container} onTouchEnd={() => this.props.navigation.navigate('Dietary')}>

                <Animated.View style={{flex: this.state.topImage}}></Animated.View>
                <ImageBackground 
                    source={require('../img/chef.png')} 
                    style={[styles.image, {flex: 5}]} 
                    imageStyle={{ borderRadius: 25 }} >
                        <Text category='h1'
                            style={{marginLeft:70, marginRight:70, color: 'white', fontWeight: 'bold'}}>
                            Choices
                        </Text>
                </ImageBackground>
                <Animated.View style={{flex: this.state.botImage}}></Animated.View>
            
                <Animated.View style={{ opacity: this.state.show, position: 'absolute', bottom: 300 }}>
                    <Text category="h3" style={{textAlign: 'center'}}>
                        Welcome to a {"\n"}
                        <Text category="h3" status="primary">
                            new food experience
                        </Text>
                    </Text>
                </Animated.View>
                

                <Animated.View
                    style={{
                        opacity: this.state.fadeAnim, // Bind opacity to animated value
                        position: 'absolute',
                        bottom: 100
                    }}
                >
                    <Text style={{color: 'white'}} category="p1" appearance="hint">
                        Tap to continue . . .
                    </Text>
                </Animated.View>

            </View>
        );
    }
}