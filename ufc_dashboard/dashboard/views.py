from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from django.http import JsonResponse
import plotly.express as px
import numpy as np

# Load and preprocess data
data_path = '../data/merged_ufc_data.csv'
df = pd.read_csv(data_path)
df = df.dropna(subset=['date'])

df['date'] = pd.to_datetime(df['date'])
df['fight_id'] = df.apply(lambda row: f"{row['date'].date()}_{row['R_fighter']}_vs_{row['B_fighter']}", axis=1)

def intro_view(request):
    return render(request, 'dashboard/intro.html')

def dashboard_view(request):
    fights = df[['fight_id', 'date', 'R_fighter', 'B_fighter']].drop_duplicates()
    fights['label'] = fights.apply(lambda row: f"{row['date'].date()} - {row['R_fighter']} vs. {row['B_fighter']}", axis=1)
    fight_options = [{'label': row['label'], 'value': row['fight_id']} for _, row in fights.iterrows()]

    context = {
        'fight_options': fight_options
    }
    return render(request, 'dashboard/dashboard.html', context)

def update_fight_info(request):
    fight_id = request.GET.get('fight_id')
    if not fight_id:
        return JsonResponse({'error': 'No fight ID provided'}, status=400)

    try:
        selected_fight_data = df[df['fight_id'] == fight_id].iloc[0]
    except IndexError:
        return JsonResponse({'error': 'Fight data not found for the given ID'}, status=404)

    ppv = int(selected_fight_data['PPV'])

    red_metrics = {
        'Significant Strikes': int(selected_fight_data['R_avg_SIG_STR_att']),
        'Takedown Attempts': int(selected_fight_data['R_avg_TD_att']),
        'Knockdowns': int(selected_fight_data['R_avg_KD'])
    }

    blue_metrics = {
        'Significant Strikes': int(selected_fight_data['B_avg_SIG_STR_att']),
        'Takedown Attempts': int(selected_fight_data['B_avg_TD_att']),
        'Knockdowns': int(selected_fight_data['B_avg_KD'])
    }

    # Update red corner bar chart
    red_fig = go.Figure(data=[go.Bar(
        x=list(red_metrics.keys()),
        y=list(red_metrics.values()),
        marker=dict(
            color=list(red_metrics.values()),  # Set color based on values
            colorscale='Reds',
            line=dict(color='rgba(255, 99, 71, 1.0)', width=2)
        ),
        name='Red Corner'
    )])
    red_fig.update_layout(
        title='Red Corner Metrics',
        yaxis_title='Metric Value',
        plot_bgcolor='#2a2a3c',
        paper_bgcolor='#2a2a3c',
        font=dict(color='#e0e0e0'),
        transition=dict(duration=500, easing='cubic-in-out')
    )

    # Update blue corner bar chart
    blue_fig = go.Figure(data=[go.Bar(
        x=list(blue_metrics.keys()),
        y=list(blue_metrics.values()),
        marker=dict(
            color=list(blue_metrics.values()),  # Set color based on values
            colorscale='Blues',
            line=dict(color='rgba(0, 123, 255, 1.0)', width=2)
        ),
        name='Blue Corner'
    )])
    blue_fig.update_layout(
        title='Blue Corner Metrics',
        yaxis_title='Metric Value',
        plot_bgcolor='#2a2a3c',
        paper_bgcolor='#2a2a3c',
        font=dict(color='#e0e0e0'),
        transition=dict(duration=500, easing='cubic-in-out')
    )

    return JsonResponse({
        'fight_name': f"{selected_fight_data['R_fighter']} vs. {selected_fight_data['B_fighter']}",
        'ppv': ppv,
        'red_chart': red_fig.to_plotly_json(),
        'blue_chart': blue_fig.to_plotly_json()
    })

def update_fight_info(request):
    try:
        fight_id = request.GET.get('fight_id')
        if not fight_id:
            return JsonResponse({'error': 'No fight ID provided'}, status=400)

        # Get the selected fight data
        selected_fight_data = df[df['fight_id'] == fight_id].iloc[0]

        ppv = int(selected_fight_data['PPV'])

        # Define red and blue metrics
        red_metrics = {
            'Significant Strikes': int(selected_fight_data['R_avg_SIG_STR_att']),
            'Takedown Attempts': int(selected_fight_data['R_avg_TD_att']),
            'Knockdowns': int(selected_fight_data['R_avg_KD'])
        }

        blue_metrics = {
            'Significant Strikes': int(selected_fight_data['B_avg_SIG_STR_att']),
            'Takedown Attempts': int(selected_fight_data['B_avg_TD_att']),
            'Knockdowns': int(selected_fight_data['B_avg_KD'])
        }

        # Create the red corner bar chart using a colorscale
        red_fig = go.Figure(data=[go.Bar(
            x=list(red_metrics.keys()),
            y=list(red_metrics.values()),
            marker=dict(
                color=list(red_metrics.values()),  # Use metric values for colorscale
                colorscale='Reds',  # Apply colorscale
                colorbar=dict(title='Metric Value')
            ),
            name='Red Corner'
        )])
        red_fig.update_layout(
            title='Red Corner Metrics',
            yaxis_title='Metric Value',
            plot_bgcolor='#2a2a3c',
            paper_bgcolor='#2a2a3c',
            font=dict(color='#e0e0e0'),
            transition=dict(duration=500, easing='cubic-in-out')
        )

        # Create the blue corner bar chart using a colorscale
        blue_fig = go.Figure(data=[go.Bar(
            x=list(blue_metrics.keys()),
            y=list(blue_metrics.values()),
            marker=dict(
                color=list(blue_metrics.values()),  # Use metric values for colorscale
                colorscale='Blues',  # Apply colorscale
                colorbar=dict(title='Metric Value')
            ),
            name='Blue Corner'
        )])
        blue_fig.update_layout(
            title='Blue Corner Metrics',
            yaxis_title='Metric Value',
            plot_bgcolor='#2a2a3c',
            paper_bgcolor='#2a2a3c',
            font=dict(color='#e0e0e0'),
            transition=dict(duration=500, easing='cubic-in-out')
        )

        return JsonResponse({
            'fight_name': f"{selected_fight_data['R_fighter']} vs. {selected_fight_data['B_fighter']}",
            'ppv': ppv,
            'red_chart': red_fig.to_plotly_json(),
            'blue_chart': blue_fig.to_plotly_json()
        })

    except Exception as e:
        print(f"Error in update_fight_info: {e}")
        return JsonResponse({'error': 'An error occurred while updating fight info.'}, status=500)


def trend_analysis(request):
    try:
        filtered_df = df.copy()

        filtered_df['total_sig_strikes'] = filtered_df['R_avg_SIG_STR_att'] + filtered_df['B_avg_SIG_STR_att']
        filtered_df['total_takedowns'] = filtered_df['R_avg_TD_att'] + filtered_df['B_avg_TD_att']

        filtered_df['high_sig_strikes'] = filtered_df['total_sig_strikes'] > filtered_df['total_sig_strikes'].mean()
        filtered_df['high_takedowns'] = filtered_df['total_takedowns'] > filtered_df['total_takedowns'].mean()

        sig_strikes_filter = request.GET.get('sig_strikes', 'all')
        takedowns_filter = request.GET.get('takedowns', 'all')

        if sig_strikes_filter != 'all':
            filtered_df = filtered_df[filtered_df['high_sig_strikes'] == (sig_strikes_filter == 'high')]
        if takedowns_filter != 'all':
            filtered_df = filtered_df[filtered_df['high_takedowns'] == (takedowns_filter == 'high')]

        scatter_fig = px.scatter(
            filtered_df, x='total_sig_strikes', y='PPV', trendline='ols',
            title='Total Significant Strikes vs. PPV',
            labels={'total_sig_strikes': 'Total Significant Strikes', 'PPV': 'PPV Buys'},
            color_discrete_sequence=['#2ecc71']
        )
        scatter_fig.update_traces(marker=dict(size=10, symbol='circle-open', line=dict(width=2, color='#27ae60')))
        scatter_fig.update_layout(
            plot_bgcolor='#2a2a3c',
            paper_bgcolor='#2a2a3c',
            font=dict(color='#e0e0e0'),
            transition=dict(duration=500, easing='cubic-in-out')
        )

        scatter_plot = scatter_fig.to_plotly_json()
        scatter_plot['data'] = [convert_ndarray_to_list(trace) for trace in scatter_plot['data']]
        scatter_plot['layout'] = convert_ndarray_to_list(scatter_plot['layout'])

        avg_ppv_data = filtered_df.groupby(['high_sig_strikes', 'high_takedowns'])['PPV'].mean().reset_index()
        avg_ppv_data['category'] = avg_ppv_data.apply(
            lambda row: 'High Sig Strikes' if row['high_sig_strikes'] and not row['high_takedowns'] else (
                'High Takedowns' if row['high_takedowns'] and not row['high_sig_strikes'] else (
                    'Both High' if row['high_sig_strikes'] and row['high_takedowns'] else 'Both Low'
                )
            ), axis=1
        )

        bar_fig = px.bar(
            avg_ppv_data, x='category', y='PPV',
            title='Average PPV by High/Low Significant Strikes and Takedowns',
            labels={'PPV': 'Average PPV'},
            color='category',
            color_discrete_map={
                'High Sig Strikes': 'red',
                'High Takedowns': 'blue',
                'Both High': 'purple',
                'Both Low': 'gray'
            }
        )
        bar_fig.update_layout(
            plot_bgcolor='#2a2a3c',
            paper_bgcolor='#2a2a3c',
            font=dict(color='#e0e0e0'),
            transition=dict(duration=500, easing='cubic-in-out')
        )

        bar_chart = bar_fig.to_plotly_json()
        bar_chart['data'] = [convert_ndarray_to_list(trace) for trace in bar_chart['data']]
        bar_chart['layout'] = convert_ndarray_to_list(bar_chart['layout'])

        return JsonResponse({
            'scatter_plot': scatter_plot,
            'bar_chart': bar_chart
        })

    except Exception as e:
        print(f"Error in trend_analysis: {e}")
        return JsonResponse({'error': 'An error occurred while processing trend analysis.'}, status=500)

def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarray_to_list(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarray_to_list(i) for i in obj]
    else:
        return obj
