import { ActionTypes } from '../../common/constants/action-types';
import { STATUS_ERROR_400, STATUS_ERROR_401, STATUS_ERROR_422, SUCCESS_200, URL_BASE } from '../../util';
import Cookies from 'js-cookie';
import * as R from 'ramda';

const fetchCredentials = (url, args) => fetch(url, {
  credentials: 'include',
  cache: 'no-cache',
  redirect: 'follow', ...args,
});

const transformResponse = R.cond([
  [
    R.compose(
      R.equals(STATUS_ERROR_400),
      R.prop('status'),
    ),
    R.always(new Error('A required parameter was missing.')),
  ],
  [
    R.compose(
      R.equals(STATUS_ERROR_401),
      R.prop('status'),
    ),
    R.always(
      new Error(
        'The request did not include the required authentication tokens.',
      ),
    ),
  ],
  [
    R.compose(
      R.equals(STATUS_ERROR_422),
      R.prop('status'),
    ),
    res => res.json(),
  ],
  [
    R.compose(
      R.equals(SUCCESS_200),
      R.prop('status'),
    ),
    res => res.json(),
  ],
  [R.T, R.always(new Error('unexpected error occurred.'))],
]);

const datasets_get = (perPage, orderBy, orderDir, page, dataset_id) => {
  const params = { perPage, orderBy, orderDir, page };
  const fetchCredentials = (url, args) => fetch(url, {
    credentials: 'include',
    cache: 'no-cache',
    redirect: 'follow', ...args,
  });

  if (dataset_id) {
    params.dataset_id = dataset_id;
  }
  const url = new URL(`${URL_BASE}/${process.env.REACT_APP_API_PDP2_GET_DATASETS_EP}`)

  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
  return fetchCredentials(url
    ,
    {
      method: 'GET',
      cache: 'no-cache',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
    },
  ).then(transformResponse)

}


export function getPdp2Datasets(
  {
    perPage,
    orderBy,
    orderDir,
    page,
    dataset_id,
  },
) {

  return dispatch => {

    dispatch({
      type: ActionTypes.GET_PDP2_DATASETS_LIST_REQUEST,
    });

    datasets_get(perPage, orderBy, orderDir, page+1, dataset_id).then( (response) => {
      dispatch({

        type: ActionTypes.GET_PDP2_DATASETS_LIST_SUCCESS,
        payload: response,
      });
    })
      .catch(error => {

        dispatch({
          type: ActionTypes.GET_PDP2_DATASETS_LIST_FAILURE,
          payload: error.response ? `${error.response.status} ${error.response.statusText}` : {},
        });
      });
  };
}