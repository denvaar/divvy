import React from 'react';
import { Route, IndexRoute } from 'react-router';


/**
* @desc routes for our application
*/
export default (
  <Route path="/" component={Main}>
    <IndexRoute component={Login} />
  </Route>
);

