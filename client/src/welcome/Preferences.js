import React, {Component} from 'react';
import {View, StyleSheet, FlatList, TouchableOpacity, Animated, Easing} from 'react-native';
import {Collapse, CollapseHeader, CollapseBody} from "accordion-collapse-react-native";
import { Text, Button, Modal, Card } from '@ui-kitten/components';

const AnimatedButton = Animated.createAnimatedComponent(TouchableOpacity);
const AnimatedModal = Animated.createAnimatedComponent(Modal);


foods = [
  {'Italian': ['Risotto', 'Tiramisu', 'Arancini', 'Gelato', 'Polenta', 'Ribollita', 'Lasagne', 'Prosciutto', 'Panini', 'Parmigiana', 'Minestrone', 'Fettuccine Alfredo', 'Margherita Pizza']},
  {'Chinese': ['Sweet and Sour Pork', 'Kung Pao Chicken', 'Ma Po Tofu', 'Wontons', 'Dumplings', 'Chow Mein', 'Peking Roasted Duck', 'Spring Rolls']},
  {'Mexican': ['Burrito', 'Carne Asada', 'Quesadilla', 'Chilaquiles', 'Taco', 'Birria', 'Tostada']},
  {'Japanese': ['Sushi', 'Tempura', 'Yakitori', 'Tsukemono pickles', 'Kaiseki', 'Udon', 'Soba', 'Sukiyaki', 'Sashimi', 'Miso soup']},
  {'Indian': ['Butter Chicken', 'Tandoori Chicken', 'Chicken Tikka Masala', 'Red Lamb', 'Malai Kofta', 'Chole', 'Palak Paneer', 'Kaali Daal', 'Papdi Chaat', 'Naan']},
  {'American': ['Apple Pie', 'Hamburger', 'Clam Chowder', 'Bagel and Lox', 'Deep-Dish Pizza', 'Drop Biscuits and Sausage Gravy', 'Texas Barbecue', 'Hominy Grits', 'Buffalo Chicken Wings']},
  {'Mediterranean': ['Feta', 'Lentils & Yogurt', 'Spanakopita', 'Baba Ganoush', 'Hummus', 'Mediterranean Cobb Salad', 'Paella', 'Fish', 'Ratatouille', 'Greek Gyros', 'Tuscan Chicken']},
  {'Thai': ['Tom Yum Goong', 'Som tum', 'Tom kha kai', 'Gaeng daeng', 'Pad Thai','Khao Pad', 'Pad krapow moo', 'Gaeng keow wan kai', 'Yum nua', 'Kai med ma muang']},
  {'Vietnamese': ['Pho', 'Banh Mi', 'Banh Xeo', 'Goi Cuon', 'Mi Quang', 'Bun Thit Nuong', 'Com Tam', 'Banh Cuon', 'Xoi Xeo', 'Ca Kho To']},
  {'French': ['Bouillabaisse', 'Quiche Lorraine', 'Steak-Frites', 'Coq au vin', 'Bœuf Bourguignon', 'Cassoulet', 'Escargots de Bourgogne', 'Moules mariníères', 'Choucroute Garnie', 'Sole Meunière']},
  {'Greek': ['Souvlaki', 'Moussaka', 'Meat balls', 'Dolmadakia', 'Taramasalata', 'Greek salad', 'Fasolada', 'Gemista', 'Spanakopita']},
];

const Header = (props) => (
    <View {...props}>
      <Text category='h5'>What foods do you like?</Text>
    </View>
);

class Cuisine extends Component {
  state = {}

  onBubbleClick = (evt, item) => {

    let xPos = evt.nativeEvent.locationX;
    let width = item.width;
    let val = item.animated_value;

    let percentage = Math.round(((xPos / width) * 100) / 20) * 20;

    Animated.timing(val, {
       toValue: percentage,
       duration: 500
    }).start();

    item.rating = percentage / 20;
    item.checked = percentage !== 0
  };

  render() {
    const interpolateWidth = val => {
      return val.interpolate({
        inputRange: [0, 100],
        outputRange: ['0%', '100%']
      })
    };

    const getWidth = val => {
        return {
            width: interpolateWidth(val),
        }
    };

    let foods_comp = []
    let cu = foods[this.props.in][this.props.name]
    for (let i = 0; i < cu.length - 1; i++) {
      foods_comp.push(
        <TouchableOpacity key = {i.toString()} 
                style = {styles.bubble}
                onLayout = {evt => foods[this.props.in][this.props.name][i].width = evt.nativeEvent.layout.width} 
                onPress = {evt => this.onBubbleClick(evt, foods[this.props.in][this.props.name][i])}>
                    <Animated.View style=
                        {[styles.bubbleFill, getWidth(cu[i].animated_value)]}
                    ></Animated.View>
                    <Text style = {styles.food_item}>{cu[i].dishName}</Text>
        </TouchableOpacity>
      )
    }
    const setCollapsed = (isCollapsed) => {
      cu[cu.length - 1] = isCollapsed;
    };
    return (

      <Collapse
  	        isCollapsed={cu[cu.length - 1]}
  	        onToggle={(isCollapsed)=> setCollapsed(isCollapsed)}>
              <CollapseHeader>
                <View style = {styles.header}><Text>{this.props.name}</Text></View>
              </CollapseHeader>
              <CollapseBody>
                {foods_comp}
              </CollapseBody>
      </Collapse>
    )
  }
}

export default class Preferences extends Component{
  constructor(props) {
    super(props);
    console.disableYellowBox = true;

    foods.forEach( cuisine => {
      for(var k in cuisine) {
        cuisine[k] = cuisine[k].map((dish, index) => {
          return {
            id: index.toString(),
            dishName: dish,
            checked: false,
            animated_value: new Animated.Value(0),
          }
        })
        cuisine[k].push(false)
        break;
      }
    })

    this.savePrefrences = this.savePrefrences.bind(this);

    this.state = {modalVisible: true, modal_pos: new Animated.Value(100)};
  }

  componentDidMount() {
    this.openModal();
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

  savePrefrences = async () => {
    console.log('save pref');
    // store in AsyncStorage

    let data = []
    foods.forEach(item => {
      let itemArr = item[Object.keys(item)[0]]
      itemArr.forEach(food => {
        if(food != false && food.dishName !== undefined && food.checked) {
          data.push([food.dishName, food.rating])
        }
      })
    })

    data = {'preferences': data}

    
    if (this.props.navigation.state.params !== undefined) {
        Object.assign(data, this.props.navigation.state.params)
    }
    
    console.log(data);

    try {
      //await AsyncStorage.setItem('@prefrences', JSON.stringify(data))
    } catch (e) {
      // saving error
      console.log(e);
    }

    // navigate to scan page
    //this.props.navigation.navigate('Scan');
  }

  render() {
    // <Cuisine cuisineIndex = index />
    return (
      <View style = {styles.container}>
        <View style={{flex: 1, alignContent: 'center', justifyContent: 'center'}}>
            <Text category='h2' style={styles.title}>
                    Preferences
            </Text>
        </View>
        <View style={{flex: 4}}>
            <FlatList
                data = {foods}
                contentContainerStyle={{flexGrow: 0.5, justifyContent: 'space-evenly'}}
                renderItem = {({ item, index }) => <Cuisine in = {index} name = {Object.keys(item)[0]}/>}
                keyExtractor={(item,index) => index.toString()}
            />
        </View>

        <View style={{
            flex: 1,
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <Button
                status='primary' size='large'
                onPress={this.savePrefrences}  >
                Submit
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
                <Text category='p1'> Just tap on each of the following cuisines and 
                    rate the foods that you've tried before by <Text category='p2'>tapping</Text> it's bubble.</Text>
                <View style={{ marginTop: '10%' }}>
                    <Button style={{marginHorizontal: 2}} onPress={this.closeModal}>
                        Get started!
                    </Button>
                </View>
            </Card>
        </AnimatedModal>

      </View>
    );
  }
}

const styles = StyleSheet.create({
  customBtnText: {
    fontSize: 30,
    color: '#00b5ec',
    fontWeight: 'bold',
    alignItems:'center',
    justifyContent: 'center',
  },
  customBtnBG: {
    backgroundColor: '#e45f1c',
    paddingHorizontal: 15,
    paddingVertical: 2,
    
    borderRadius: 30,
    marginBottom: 40,
    alignItems:'center',
    justifyContent: 'center',
  },
  container: {
    ...StyleSheet.absoluteFillObject,
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00b5ec',
  },
  title: {
    color: '#FFFCE4', 
    padding: 30, 
    fontWeight: 'bold'
  },
  header: {
      marginBottom: 20,
      backgroundColor: '#FFFFFF',
      borderRadius:15,
      width:250,
      height:30,
      alignItems:'center',
      alignSelf: 'flex-start',
      justifyContent: 'center',
  },
  bubble: {
      backgroundColor: 'rgb(255, 205, 145)',
      borderRadius: 30,
      overflow: 'scroll',
      marginTop: 5,
    //   marginLeft: 25,
      marginBottom: 5,
  },
  bubbleFill: {
      width: '0%',
      backgroundColor: 'rgb(228,95,28)', 
      position: 'absolute', 
      height: '100%', 
      borderRadius: 30
    },  
  food_item: {
    color: '#001f3f',
    fontWeight: 'bold',
    textAlign: 'center'
  }
})
