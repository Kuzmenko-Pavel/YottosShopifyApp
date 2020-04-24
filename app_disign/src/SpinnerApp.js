import React from "react";

export default function SpinnerApp() {
    return (
        <div>
            <div style={{
                position: 'absolute',
                left: '50%',
                top: '50%'
            }}>
                <img
                    src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgNDQgNDQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTE1LjU0MiAxLjQ4N0EyMS41MDcgMjEuNTA3IDAgMDAuNSAyMmMwIDExLjg3NCA5LjYyNiAyMS41IDIxLjUgMjEuNSA5Ljg0NyAwIDE4LjM2NC02LjY3NSAyMC44MDktMTYuMDcyYTEuNSAxLjUgMCAwMC0yLjkwNC0uNzU2QzM3LjgwMyAzNC43NTUgMzAuNDczIDQwLjUgMjIgNDAuNSAxMS43ODMgNDAuNSAzLjUgMzIuMjE3IDMuNSAyMmMwLTguMTM3IDUuMy0xNS4yNDcgMTIuOTQyLTE3LjY1YTEuNSAxLjUgMCAxMC0uOS0yLjg2M3oiIGZpbGw9IiM5MTlFQUIiLz48L3N2Zz4K"
                    className="Polaris-Spinner Polaris-Spinner--colorTeal Polaris-Spinner--sizeLarge"
                />
                <span role="status">
                    <span className="Polaris-VisuallyHidden"></span>
            </span>
            </div>
        </div>
    );
}