import React, {Component} from 'react';
import {View, StyleSheet, Dimensions, Animated, Easing} from 'react-native';
import { Input, Card, Text, Datepicker, IndexPath, Select, SelectItem, Button, Modal } from '@ui-kitten/components';

const WIDTH = Dimensions.get('window').width;
const HEIGHT = Dimensions.get('window').height;

const AnimatedModal = Animated.createAnimatedComponent(Modal)

export const RACES = [
    'Select',
    'White', 
    'Black or African American', 
    'American Indian or Alaska Native',
    'Asian',
    'Native Hawaiian or Other Pacific Islander'
];

export const GENDERS =[
    'Select',
    'Male',
    'Female',
    'Other'
];


const styles = StyleSheet.create({
    container: {
        ...StyleSheet.absoluteFillObject,
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#00b5ec',
    },
    calendarContainer: {
        margin: 2,
    },
    text: {
        marginVertical: 8,
    },
});

const Header = (props) => (
    <View {...props}>
      <Text category='h5'>Let's get to know you!</Text>
    </View>
);

export default class Demographic extends Component {
    constructor(props) {
        super(props);

        this.state = {
            'name': '',
            'birthday': '',
            'raceIndex': new IndexPath(0),
            'genderIndex': new IndexPath(0),
            'modal_pos': new Animated.Value(100),
            'modalVisible': true,
        };
    }

    componentDidMount() {
        this.openModal();
    }

    onSubmit = () => {
        let data = {};
        if (this.state.name !== '') {
            data.name = this.state.name;
        }
        if (this.state.birthday !== '') {
            console.log(this.state.birthday);
            data.birthday = this.state.birthday;
        }
        if (this.state.raceIndex.row !== 0) {
            data.race = RACES[this.state.raceIndex.row];
        }
        if (this.state.genderIndex.row !== 0) {
            data.gender = RACES[this.state.genderIndex.row];
        }

        this.props.navigation.navigate('Preferences', data)
    }

    openModal = () => {
        let val = this.state.modal_pos;

        Animated.timing(val, {
            toValue: 0,
            easing: Easing.bounce,
            duration: 1200
        }).start();
    }

    closeModal = () => {
        let val = this.state.modal_pos;

        Animated.timing(val, {
            toValue: -40,
            duration: 300
        }).start(() => {
            Animated.timing(val, {
                toValue: 150,
                duration: 500,
            }).start(() => {
                this.setState({modalVisible: false})
            });
        });

    }
    
    render() {
        return (
            <View style={styles.container}>
                <View style={{flex: 1, alignContent: 'center', justifyContent: 'center'}}>
                    <Text category='h2'
                        style={{color: '#FFFCE4', padding: 30, fontWeight: 'bold'}}>
                        Demographics
                    </Text>
                </View>
                <View style={{flex: 4, alignItems: 'center', justifyContent: 'flex-start'}}>
                    <Card status='primary'>
                        <Input
                            style={{width: WIDTH - 150}} 
                            value={this.state.name}
                            label='Name'
                            placeholder='John Doe'
                            onChangeText={name => this.setState({ name })}
                        />

                        <Datepicker
                            placeholder='dd/mm/yyyy'
                            style={{marginTop: 20}} 
                            label='Birthday'
                            date={this.state.birthday}
                            onSelect={birthday => this.setState({ birthday: birthday.getTime() })}
                        />

                        <Select
                            label='Race'
                            style={{marginTop: 20}}
                            value={RACES[this.state.raceIndex.row]} 
                            selectedIndex={this.state.raceIndex}
                            onSelect={raceIndex => this.setState({raceIndex})}>
                            { RACES.map((race, index) => {
                                    return (
                                        <SelectItem key={index} title={race} />
                                    )
                            })}
                        </Select>

                        <Select
                            label='Gender'
                            style={{marginTop: 20}}
                            value={GENDERS[this.state.genderIndex.row]} 
                            selectedIndex={this.state.genderIndex}
                            onSelect={genderIndex => this.setState({genderIndex})}>
                            { GENDERS.map((gender, index) => {
                                    return (
                                        <SelectItem key={index} title={gender} />
                                    )
                            })}
                        </Select>
                    </Card>
                </View>
                <View style={{
                        position: 'absolute',
                        bottom: 100
                    }}>
                    <Button status='primary' size='large' onPress={this.onSubmit}>
                        Continue
                    </Button>
                </View>

                <AnimatedModal
                style={{marginRight: '10%', marginTop: this.state.modal_pos.interpolate({
                    inputRange: [0, 100],
                    outputRange: ['0%', '100%']
                })}}
                visible={this.state.modalVisible}
                backdropStyle={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}
                onBackdropPress={this.closeModal}>
                <Card disabled={true} header={Header}>
                    <Text category='p2'>Luckily, we promise to never release or expose our users' personal data and take extreme technological measures to ensure this.</Text>
                    <View style={{ marginTop: '10%' }}>
                        <Button style={{marginHorizontal: 2}} onPress={this.closeModal}>
                            Got it!
                        </Button>
                    </View>
                </Card>
            </AnimatedModal>
            </View>
        );
    }
}