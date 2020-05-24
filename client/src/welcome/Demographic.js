import React, {Component} from 'react';
import {View, StyleSheet, Dimensions} from 'react-native';
import { Input, Card, Text, Datepicker, IndexPath, Select, SelectItem, Button } from '@ui-kitten/components';

const WIDTH = Dimensions.get('window').width;
const HEIGHT = Dimensions.get('window').height;

const RACES = [
    'White', 
    'Black or African American', 
    'American Indian or Alaska Native',
    'Asian',
    'Native Hawaiian or Other Pacific Islander'
];

const GENDERS =[
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
  

export default class Demographic extends Component {
    constructor(props) {
        super(props);

        this.state = {
            'name': '',
            'birthday': '',
            'raceIndex': new IndexPath(0),
            'genderIndex': new IndexPath(0),
        };
    }
    
    render() {
        return (
            <View style={styles.container}>
                <View style={{flex: 1}}>
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
                            onSelect={birthday => this.setState({ birthday })}
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
                    <Button status='primary' size='large' onPress={() => this.props.navigation.navigate('Preferences')}>
                        Continue
                    </Button>
                </View>
            </View>
        );
    }
}