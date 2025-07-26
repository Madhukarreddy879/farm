import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

const ReceiptsScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text>Receipts Screen</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
      {/* Add functionality to list and generate receipts here */}
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

export default ReceiptsScreen;
