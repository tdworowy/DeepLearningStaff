import * as React from "react";
import {
  networksEndPoint,
  deleteNetworkEndPoint,
  ExportNetworkEndPoint,
} from "./Config";
import { NetworkDetails } from "./NetworkDetails";
import ReactDOM from "react-dom";

async function getNetworks() {
  const response = await fetch(networksEndPoint, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  return await response.json();
}
async function exportNetwork(name: string) {
  const response = await fetch(ExportNetworkEndPoint + name, {
    method: "GET",
    headers: { "Content-Type": "application/octet-stream " },
  });
  return await response.blob();
}
async function deleteNetwork(name: string | File | null) {
  const response = await fetch(deleteNetworkEndPoint, {
    method: "Delete",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name }),
  });
  return await response.json();
}
function deleteNetworkHandler(name: string) {
  return () => {
    console.log(`Delete:${name}`);
    deleteNetwork(name).then((data) => {
      console.log(`Response:${JSON.stringify(data)}`);
    });
  };
}
function exportNetworkHandler(name: string) {
  return () => {
    console.log(`Export:${name}`);
    exportNetwork(name).then((data) => {
      const fileName = name + ".hdf5";
      console.log(`Download:${fileName}`);

      const objectUrl: string = URL.createObjectURL(data);
      const a: HTMLAnchorElement = document.createElement(
        "a"
      ) as HTMLAnchorElement;

      a.href = objectUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();

      document.body.removeChild(a);
      URL.revokeObjectURL(objectUrl);
    });
  };
}
interface networkData {
  name: string;
  compiled: boolean;
  trained: boolean;
}
type State = { networks: Array<networkData> };
export class NetworksList extends React.Component<{}, State> {
  timer: any;

  constructor(props: any) {
    super(props);
    this.state = {
      networks: [],
    };
  }
  componentDidMount() {
    this.timer = setInterval(
      () =>
        getNetworks().then((data) => {
          if (data.Networks !== "") {
            console.log(`Response:${JSON.stringify(data.Networks)}`);
            this.setState({ networks: data.Networks });
          }
        }),
      10000
    );
  }

  createNetworkList = () => {
    let networks: Array<JSX.Element> = [];
    if (this.state.networks.length > 0) {
      this.state.networks.forEach(function (value) {
        console.log(value);
        networks.push(
          <tr id={value.name}>
            <td>
              <label>{value.name}</label>
            </td>
            <td>
              <button
                id="details"
                onClick={(event) =>
                  ReactDOM.render(
                    <NetworkDetails params={value.name} />,
                    document.getElementById("root")
                  )
                }
              >
                Details
              </button>
            </td>
            <td>
              <button id="delete" onClick={deleteNetworkHandler(value.name)}>
                Delete
              </button>
            </td>
            <td>
              <button id="export" onClick={exportNetworkHandler(value.name)}>
                Export
              </button>
            </td>
            <td id={String(value.compiled)}>
              <label id="compiled">{String(value.compiled)}</label>
            </td>
            <td id={String(value.trained)}>
              <label id="trained">{String(value.trained)}</label>
            </td>
          </tr>
        );
      });
    }
    return networks;
  };

  render() {
    return (
      <div>
        <table title="Networks:">
          <tbody>
            <tr>
              <th>Network name</th>
              <th>Details</th>
              <th>Delete</th>
              <th>Export</th>
              <th>Compiled</th>
              <th>Trained</th>
            </tr>
            {this.createNetworkList()}
          </tbody>
        </table>
      </div>
    );
  }
}
