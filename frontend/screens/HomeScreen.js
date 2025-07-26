import React from "react";
import { View, Text, StyleSheet, Button, Alert } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const HomeScreen = ({ navigation }) => {
  const handleLogout = async () => {
    Alert.alert(
      "Logout",
      "Are you sure you want to log out?",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Logout",
          onPress: async () => {
            await AsyncStorage.removeItem("accessToken");
            navigation.replace("Login"); // Go back to login screen
          },
        },
      ],
      { cancelable: false },
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to the Farm Management App!</Text>
      <View style={styles.buttonContainer}>
        <Button
          title="Register Farmer"
          onPress={() => navigation.navigate("FarmerRegistration")}
        />
        <Button
          title="Seed Distribution"
          onPress={() => navigation.navigate("SeedDistribution")}
        />
        <Button
          title="Harvest Entry"
          onPress={() => navigation.navigate("HarvestEntry")}
        />
        <Button
          title="View Receipts"
          onPress={() => navigation.navigate("Receipts")}
        />
        <View style={styles.logoutButton}>
          <Button
            title="Logout"
            onPress={handleLogout}
            color="#FF6347" // Tomato color for logout button
          />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    backgroundColor: "#f5f5f5",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 30,
    color: "#333",
  },
  buttonContainer: {
    width: "100%",
    maxWidth: 300,
    gap: 10, // Adds space between buttons
  },
  logoutButton: {
    marginTop: 20, // Space above logout button
  },
});

export default HomeScreen;
