import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

const FarmerRegistrationScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text>Farmer Registration Screen</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
      {/* Add form for farmer registration here */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default FarmerRegistrationScreen;
