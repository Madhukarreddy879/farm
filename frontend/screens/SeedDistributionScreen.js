import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

const SeedDistributionScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text>Seed Distribution Entry Screen</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
      {/* Add form for seed distribution entry here */}
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

export default SeedDistributionScreen;
