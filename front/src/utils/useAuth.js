import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import Login from "src/pages/Login";

const authContext = React.createContext();

export function useAuth() {
  const [authed, setAuthed] = React.useState({});
  const USER = "USER"

  React.useEffect(() => {
    try {
      var o = JSON.parse(localStorage.getItem(USER))
      if (o && typeof o === "object")
        setAuthed(o)
    } catch (e) {
    }
  }, [])


  return {
    authed,
    login(data) {
      return new Promise((res) => {
        localStorage.setItem(USER, JSON.stringify(data))
        setAuthed(data);
        res();
      });
    },
    logout() {
      return new Promise((res) => {
        localStorage.setItem(USER, JSON.stringify({}))
        setAuthed({});
        res();
      });
    }
  };
}

export function AuthProvider({ children }) {
  const auth = useAuth();

  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export default function AuthConsumer() {
  return React.useContext(authContext);
}


export function RequireAuth({ children }) {
  const { authed } = useAuth();
  const location = useLocation();

  return authed?.object_type ? (
    children
  ) : (
    <>
      <Login />
    </>
  );
}
