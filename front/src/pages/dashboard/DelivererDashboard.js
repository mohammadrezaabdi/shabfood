
import React from 'react'
import { filter } from 'lodash';
import { sentenceCase } from 'change-case';
import {
  Card,
  Table,
  Stack,
  TableRow,
  TableBody,
  TableCell,
  Container,
  Typography,
  TableContainer,
  TablePagination
} from '@mui/material';
import Page from '../../components/helpers/Page';
import Label from '../../components/helpers/Label';
import { getDelivererCurrent, getDelivererRequest } from 'src/utils/requests'
import Scrollbar from '../../components/helpers/Scrollbar';
import SearchNotFound from '../../components/helpers/SearchNotFound';
import { CustomerDashboardListHead, CustomerDashboardListToolbar, } from '../components/CustomerDashboard';
import { useAuth } from 'src/utils/useAuth';
import { orderStateToColor, orderStateToStr, USER_TYPES } from 'src/utils/values';
import { useNavigate } from 'react-router-dom';
import DelivererDashboardMoreMenu from '../components/RestaurantDashboard/DelivererDashboardMoreMenu';

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'customerID', label: 'Customer', alignRight: false },
  { id: 'restAddr', label: 'Restaurant address', alignRight: false },
  { id: 'addr', label: 'Destination', alignRight: false },
  { id: 'status', label: 'Status', alignRight: true },
  { id: 'action', label: 'Action', alignRight: true },
];

// ----------------------------------------------------------------------
function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(array, comparator, query) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query) {
    return filter(array, (_user) => _user.customerID.toLowerCase().indexOf(query.toLowerCase()) !== -1);
  }
  return stabilizedThis.map((el) => el[0]);
}

// ----------------------------------------------------------------------

export default function DelivererDashboard() {
  const [orders, setOrders] = React.useState([])
  const [requestOrder, setRequestOrder] = React.useState({})
  const [currentOrder, setCurrentOrder] = React.useState({})
  const [refreshKey, setRefreshKey] = React.useState(0)



  const { authed, logout } = useAuth({});
  const navigate = useNavigate();
  React.useEffect(() => {
    if (!!authed?.access_token)
      getDelivererRequest(authed?.access_token)
        .then(res => {
          setRequestOrder(res?.data)
        })
        .catch((e) => {
          if (e?.response?.status + "" === "401") {
            logout()
            navigate('/login', { replace: true });
          }
          setRequestOrder({})
        })

  }, [authed, refreshKey])

  React.useEffect(() => {
    if (!!authed?.access_token)
      getDelivererCurrent(authed?.access_token)
        .then(res => {
          setCurrentOrder(res?.data)
        })
        .catch((e) => {
          if (e?.response?.status + "" === "401") {
            logout()
            navigate('/login', { replace: true });
          }
          setCurrentOrder({})
        })

  }, [authed, refreshKey])

  React.useEffect(() => {
    setOrders([
      currentOrder,
      requestOrder
    ].filter(row => !!row?.id)
      .map(row => ({
        id: row?.id,
        time: row?.timestamp,
        status: row?.status,
        addr: row?.customer?.address,
        customerID: row?.customer?.id,
        restName: row?.restaurant?.name,
        restAddr: row?.restaurant?.address,
        restId: row?.restaurant?.id,
      })))
  }, [currentOrder, requestOrder])

  const handleRefreshRequest = () => {
    setRefreshKey(oldkey => oldkey + 1)
  }


  const [page, setPage] = React.useState(0);
  const [order, setOrder] = React.useState('desc');
  const [orderBy, setOrderBy] = React.useState('time');
  const [filterName, setFilterName] = React.useState('');
  const [rowsPerPage, setRowsPerPage] = React.useState(5);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleFilterByName = (event) => {
    setFilterName(event.target.value);
  };

  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - orders.length) : 0;

  const filteredMenu = applySortFilter(orders, getComparator(order, orderBy), filterName);

  return (
    <>
      <Page title="Dashboard">
        <Container>
          <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
            <Typography variant="h4" gutterBottom>
              Deliverer Dashboard
            </Typography>
          </Stack>

          <Card>
            <CustomerDashboardListToolbar
              filterName={filterName}
              onFilterName={handleFilterByName}
            />

            <Scrollbar>
              <TableContainer sx={{ minWidth: 800 }}>
                <Table>
                  <CustomerDashboardListHead
                    order={order}
                    orderBy={orderBy}
                    headLabel={TABLE_HEAD}
                    onRequestSort={handleRequestSort}
                    handleRefresh={handleRefreshRequest}
                  />
                  <TableBody>
                    {filteredMenu
                      .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                      .map((row) => {
                        const { id, customerID, time, status, addr, restAddr } = row;
                        const color = orderStateToColor[status + ""] || "error"
                        let statusStr = orderStateToStr[status + ""] || ""

                        return (
                          <TableRow
                            hover
                            key={id}
                            tabIndex={-1}
                            role="checkbox"
                          >
                            <TableCell padding="checkbox">
                              {/* <IconButton onClick={refreshKey} color='primary' disabled={status === 0}>
                              <Icon icon={plusCircleOutlined} width={20} height={20} />
                            </IconButton> */}
                            </TableCell>
                            <TableCell align="left">{customerID}</TableCell>
                            <TableCell align="left">{restAddr}</TableCell>
                            <TableCell align="left">{addr}</TableCell>
                            <TableCell align="right">
                              <Label
                                variant="ghost"
                                color={color}
                              >
                                {sentenceCase(statusStr)}
                              </Label>
                            </TableCell>
                            <TableCell align="right">
                              <DelivererDashboardMoreMenu
                                orderID={id}
                                currentStatus={status + ""}
                                handleRefresh={handleRefreshRequest}
                              />
                            </TableCell>

                          </TableRow>
                        );
                      })}
                    {emptyRows > 0 && (
                      <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                      </TableRow>
                    )}
                  </TableBody>
                  {(filteredMenu.length === 0) && (
                    <TableBody>
                      <TableRow>
                        <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                          <SearchNotFound searchQuery={filterName} />
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  )}
                </Table>
              </TableContainer>
            </Scrollbar>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={orders.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </Card>
        </Container>
      </Page>
    </>
  );
}


