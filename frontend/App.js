import "react-native-gesture-handler";
import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { StatusBar } from "expo-status-bar";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { ActivityIndicator, View, StyleSheet } from "react-native";

import LoginScreen from "./screens/LoginScreen";
import HomeScreen from "./screens/HomeScreen";
import FarmerRegistrationScreen from "./screens/FarmerRegistrationScreen";
import SeedDistributionScreen from "./screens/SeedDistributionScreen";
import HarvestEntryScreen from "./screens/HarvestEntryScreen";
import ReceiptsScreen from "./screens/ReceiptsScreen";

const Stack = createStackNavigator();

// AuthLoadingScreen to check for token and redirect
function AuthLoadingScreen({ navigation }) {
  React.useEffect(() => {
    const checkToken = async () => {
      const userToken = await AsyncStorage.getItem("accessToken");
      navigation.replace(userToken ? "Home" : "Login");
    };
    checkToken();
  }, []);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="AuthLoading">
        <Stack.Screen
          name="AuthLoading"
          component={AuthLoadingScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
          name="FarmerRegistration"
          component={FarmerRegistrationScreen}
          options={{ title: "Register Farmer" }}
        />
        <Stack.Screen
          name="SeedDistribution"
          component={SeedDistributionScreen}
          options={{ title: "Seed Distribution Entry" }}
        />
        <Stack.Screen
          name="HarvestEntry"
          component={HarvestEntryScreen}
          options={{ title: "Harvest Entry" }}
        />
        <Stack.Screen
          name="Receipts"
          component={ReceiptsScreen}
          options={{ title: "Farmer Receipts" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
