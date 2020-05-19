import React, {Component, useRef, useEffect} from 'react';
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
        flex: 1,
        width: 300,
        height: 300,
        resizeMode: "cover",
        justifyContent: "center",
        marginTop: 30
    },
});
  
  

export default class Welcome extends Component {

    state = {
        fadeAnim: new Animated.Value(0)
    }

    constructor(props) {
        super(props);
        this.fadeIn();
    }

    fadeIn = () => {
        // Will change fadeAnim value to 1 in 5 seconds
        Animated.timing(this.state.fadeAnim, {
          toValue: 1,
          duration: 1000
        }).start(() => this.fadeOut());
    };

    fadeOut = () => {
        // Will change fadeAnim value to 0 in 5 seconds
        Animated.timing(this.state.fadeAnim, {
            toValue: 0,
            duration: 1000
        }).start(() => this.fadeIn());
    };    
    
    render() {
        return (
            <View style={styles.container} onTouchEnd={() => this.props.navigation.navigate('Dietary')}>
                <View style={{flex: 4, justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
                    <ImageBackground 
                        source={require('../img/chef.png')} 
                        style={styles.image} 
                        imageStyle={{ borderRadius: 25 }} >
                        <Text category='h1'
                            style={{textAlign: 'center', color: 'white', marginTop: 180}}>
                            Choices
                        </Text>
                    </ImageBackground>
                </View>
                <View style={{flex: 5, justifyContent: 'flex-start', alignItems: 'center'}}>
                    <Text category="h3" style={{textAlign: 'center'}}>
                        Welcome to a {"\n"}
                        <Text category="h3" status="primary">
                            new food experience
                        </Text>
                    </Text>
                </View>

                <Animated.View
                    style={{
                        opacity: this.state.fadeAnim, // Bind opacity to animated value
                        position: 'absolute',
                        bottom: 100
                    }}
                >
                <Text style={{color: 'white'}} category="p1" appearance="hint">Tap to continue . . .</Text>
              </Animated.View>
            </View>
        );
    }
}