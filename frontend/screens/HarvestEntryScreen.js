import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

const HarvestEntryScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text>Harvest Entry Screen</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
      {/* Add form for harvest entry here */}
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

export default HarvestEntryScreen;
