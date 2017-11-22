from urllib.parse import quote
import re


class FusionTableAgent:
    embeds = {
        "integrated_network": '<iframe width="${WIDTH}" height="${HEIGHT}" scrolling="no" frameborder="no" src="https://fusiontables.google.com/embedviz?containerId=googft-gviz-canvas&amp;viz=GVIZ&amp;t=GRAPH&amp;gc=false&amp;gd=false&amp;sdb=1&amp;rmax=100000&amp;uiversion=2&amp;q=select+col0%2C+col1+from+1saTMzq23jACF0_WEh06OTJQn7PDJYPluj9IjEp-o${WHERE}&amp;qrs=+where+col0+%3E%3D+&amp;qre=+and+col0+%3C%3D+&amp;qe=&amp;state=%7B%22ps%22%3A%221_b_-45_-h_s_-4r_-i_11_-3t_-w_v_-3x_v_d_-35_8_15_-3u_1k_3_-4a_1c_j_-4h_v_p_-3o_-a_r_-59_9_1_-41_3_u_-4h_-1f_h_-4t_19_5_-4r_c_g_-3e_q_l_-50_-z_4_-5w_4_7_-4k_-2_z_-39_-q_a_-3z_-1e_k_-5n_-a_14_-54_-7_i_-3g_17_y_-3n_b_9_-49_i_e_-4f_-z_w_-64_o_16_-3c_-1a_8_-5n_k_x_-59_s_o_-5d_17_6_-2x_10_f_-5t_15_n_-4w_1u_m_-5c_1n_c_-4e_1x_2_-38_-8_0_-5e_-p_18_-2o_2_q_-5x_-r_17_-4w_p_19_-5k_-18_12_-54_-1h_t_-2q_-d_13_-2j_o_10_-5y_1o_1s_-28_-i_1b_-1t_n_1r_-2e_-15_1y_-3c_-1z_1f_-31_1i_1q_-4s_-25_1g_-69_-9_25_-2k_1k_2e_-27_-w_1o_-2s_-1r_1v_-3z_-1z_2h_-3n_-1m_24_-1p_10_1k_-5j_2a_2c_-6c_-w_1p_-2j_-r_2g_-2w_-11_22_-2p_1v_29_-3a_2d_2b_-22_-7_1u_-2o_-17_1n_-4b_2b_27_-31_27_1c_-6q_12_1m_-6n_-1_1i_-5g_2y_1a_-3i_24_2n_-5v_-1u_1z_-4g_-22_23_-1z_13_1t_-3h_-2h_21_-1z_a_2f_-61_-1m_1w_-2k_-z_2p_-6i_12_2q_-2b_c_1x_-2o_-w_2d_-3p_-2g_2a_-1o_1l_1j_-4r_36_2i_-5j_-21_1e_-6b_2d_20_-27_-2_1d_-61_2r_26_-25_1e_2j_-71_m_2k_-l_q_2l_-n_10_36_-39_-1q_1l_-7e_z_2o_-6y_1t_28_-28_1l_1h_-3e_1u_2r_-52_2n_2s_-6l_-d_2m_-5a_-f_2u_-1v_-u_2v_-1r_-b_2w_-1s_-i_2x_-71_-1d_2y_-4w_-1p_2z_-6g_-26_30_-1q_5_31_-3p_-1z_32_-5p_-2n_33_-6a_1h_34_-6c_1b_35_-5p_20_2t_-1t_-o_%22%2C%22cx%22%3A-117.7214755063955%2C%22cy%22%3A-10.296555256502627%2C%22sw%22%3A1289.5917905934296%2C%22sh%22%3A622.1714779178826%2C%22z%22%3A2.7449356685373876%7D&amp;gco_forceIFrame=true&amp;gco_hasLabelsColumn=true&amp;width=${WIDTH}&amp;height=${HEIGHT}"></iframe>',
		'shop_to_topic': '<iframe width="${WIDTH}" height="${HEIGHT}" scrolling="no" frameborder="no" src="https://fusiontables.google.com/embedviz?containerId=googft-gviz-canvas&amp;viz=GVIZ&amp;t=GRAPH&amp;gc=true&amp;gd=false&amp;sdb=1&amp;rmax=100000&amp;q=select+col0%2C+col1%2C+col2+from+1g4lIa3wr1HZ4J5JqNxCj1qy407hALyo01U-1wyD-${WHERE}&amp;qrs=+where+col0+%3E%3D+&amp;qre=+and+col0+%3C%3D+&amp;qe=&amp;uiversion=2&amp;state=%7B%22ps%22%3A%221_i_-5v_-1i_29_-6f_-3l_h_-4y_-30_2q_-74_-1t_1p_-40_-m_1_-4o_f_j_-74_-2p_n_-57_-4b_d_0_-3d_m_-4o_-3q_34_-79_-3x_1e_-5q_-3t_t_-5n_-30_k_-3m_-3l_1f_-6c_-2q_18_-6f_-7_25_-3p_-28_19_-32_12_1j_-4m_-26_q_-6a_-4j_2a_-w_-1f_2p_-3n_-1_2w_-7n_-15_1w_-4l_-4v_1m_-23_-22_1k_-q_-26_7_5c_7g_l_-5k_-27_2b_-31_-h_w_-5t_c_y_-54_-a_2h_-1i_-3i_1n_-29_-14_2o_-5y_-m_10_-k_3b_11_-18_1x_1i_93_-1r_14_-1q_3c_0_-4q_1w_e_1t_-40_r_-6f_-20_2j_8n_-6w_22_-2p_-1o_1u_-2c_2n_2x_-1t_2h_1a_-6x_-w_f_-3p_1l_1d_-20_21_1x_-2e_-3g_12_-18_2w_1v_-5x_-5l_2y_94_72_b_15_-3t_z_-72_6_2f_1e_-36_2d_16_-4i_v_-59_-5d_4_-3w_y_s_-5q_-4m_x_-56_-u_1y_-1x_-2u_1z_o_-4b_a_8o_3v_g_-1w_-d_27_91_-35_26_9g_-2k_1l_1_-1u_1b_-7p_-5_5_5m_6n_2_-46_2i_1s_66_7o_1g_-6w_-4m_p_-4j_-1j_32_9e_-y_28_8p_-2j_o_-44_-1o_2u_8d_-1b_8_9e_3q_9_9d_31_2c_-2m_8_21_8o_35_23_4j_78_1o_-2_-1c_6_5w_61_3_-53_2o_2r_-85_-1v_24_3v_76_1t_6s_7v_2e_1l_-57_1r_-37_3_2g_25_-2w_1q_-3d_-11_2i_-17_-4a_1h_9t_-1p_2k_94_-6e_2l_86_-7e_2m_85_-6g_2n_95_-7c_1c_5g_85_17_4v_7z_16_89_4e_20_o_-54_2s_-8j_82_2t_-7y_86_15_6_3n_2v_7v_-w_13_-8_42_u_-55_-2e_c_1r_-4i_2z_8s_6i_30_9r_6z_31_8v_7o_33_9k_-b_35_-7z_-4k_36_-87_-46_%22%2C%22cx%22%3A30.662587947205623%2C%22cy%22%3A-19.677142172856456%2C%22sw%22%3A961.9117571759574%2C%22sh%22%3A848.2681740496839%2C%22z%22%3A0.9953640974687907%7D&amp;gco_forceIFrame=true&amp;gco_hasLabelsColumn=true&amp;width=${WIDTH}&amp;height=${HEIGHT}"></iframe>',
		'shop_to_shop': '<iframe width="${WIDTH}" height="${HEIGHT}" scrolling="no" frameborder="no" src="https://fusiontables.google.com/embedviz?containerId=googft-gviz-canvas&amp;viz=GVIZ&amp;t=GRAPH&amp;gc=true&amp;gd=true&amp;sdb=1&amp;rmax=100000&amp;q=select+col0%2C+col1%2C+col2+from+1jxw824iar1mlckzwn896ELalzWBPuXs12mS8Hadm${WHERE}&amp;qrs=+where+col0+%3E%3D+&amp;qre=+and+col0+%3C%3D+&amp;qe=&amp;uiversion=2&amp;state=%7B%22ps%22%3A%221_1m_21_-9_14_2o_5_4_s_-i_1s_-7_g_13_b_12_2k_r_1m_2j_m_-2_u_14_3_2e_23_1g_x_s_i_28_1b_1b_0_13_x_c_5_-e_29_1c_1x_25_1t_i_a_b_8_1t_1u_-u_d_p_w_5_1z_x_24_2v_1u_j_2e_17_23_1i_-n_r_13_-y_2_1q_2q_1d_2c_1s_1f_1p_1d_n_1m_25_1_2l_1i_s_1f_t_1o_2d_s_26_14_2p_1l_1c_-c_t_2n_26_6_1j_1_g_1n_2f_i_2m_2h_l_s_26_17_1e_g_h_2h_2x_18_3a_17_q_2y_18_e_1n_z_f_2p_10_21_2d_22_10_25_e_9_c_m_m_3b_1v_1p_2b_2j_11_15_h_1v_1u_1p_1q_1b_2k_2m_2l_l_y_1r_8_1r_3d_q_2b_1w_22_2i_21_1w_2d_o_2e_w_5_0_1b_2y_n_7_18_-o_p_2k_-v_1e_3h_1n_12_37_-b_1k_3v_v_16_-8_-6_1n_24_2a_o_1n_-17_2a_3p_7_1j_26_2y_22_3p_y_v_6_2k_2l_3p_-7_3_3u_e_1u_2x_-h_b_20_2r_2g_p_2l_z_2y_2f_k_1j_-10_1y_3m_15_15_22_2n_1a_3p_25_8_2p_-g_1x_2y_-1a_1c_37_t_1g_35_-g_1h_38_2a_19_3b_-1_2f_34_1z_2c_-k_w_1i_28_2q_2n_28_-15_1w_13_-a_1z_-1n_45_20_-1e_3e_2h_-2j_1m_27_-1z_2f_%22%2C%22cx%22%3A43.99115152580889%2C%22cy%22%3A41.80897624624191%2C%22sw%22%3A607.7557064086407%2C%22sh%22%3A716.8224753916811%2C%22z%22%3A3.152656151062614%7D&amp;gco_forceIFrame=true&amp;gco_hasLabelsColumn=true&amp;width=${WIDTH}&amp;height=${HEIGHT}"></iframe>',
        'shop_location': '<iframe width="${WIDTH}" height="${HEIGHT}" scrolling="no" frameborder="no" src="https://fusiontables.google.com/embedviz?q=select+col0+from+1OYEWQIt5VRxiGCoLQP8hbdwW5stuLn6_cw_gvHyc&amp;viz=MAP&amp;h=false&amp;lat=37.497&amp;lng=127.03104330577395&amp;t=1&amp;z=14&amp;l=col0&amp;y=2&amp;tmplt=3&amp;hml=ONE_COL_LAT_LNG"></iframe>',
    }

    def __init__(self):
        return

    def get_src(self, k, width=900, height=500, filter_col=None, filters=None):
        src = self.embeds[k]
        src = src.replace('${WIDTH}', str(width))
        src = src.replace('${HEIGHT}', str(height))

        where_query = ''
        if filter_col is not None and filters is not None:
            for i, f in enumerate(filters):
                filters[i] = '&#39;' + quote(f) + '&#39;'
            where_query = '+where+%s+in+(%s)' % (filter_col, '%2C+'.join(filters))

        src = src.replace('${WHERE}', where_query)

        return src


def main():
    fta = FusionTableAgent()
    s = ''
    with open('fusion_table_network_test.html', 'w') as ofp:
        s += fta.get_src('integrated_network', 900, 500)
        s += '\n'
        s += fta.get_src('integrated_network', 900, 500,
                         filter_col='col0', filters=['커피빈강남대로점', '엔제리너스강남교보타워'])
        s += '\n'
        s += fta.get_src('shop_to_shop', 900, 500,
                         filter_col='col1', filters=['커피빈강남대로점', '엔제리너스강남교보타워'])
        s += '\n'
        s += fta.get_src('shop_to_topic', 900, 500,
                         filter_col='col0', filters=['커피빈강남대로점', '엔제리너스강남교보타워'])
        s += '\n'
        s += fta.get_src('shop_location', 900, 500)
        s += '\n'
        ofp.write(s)
        print(s)



if __name__ == '__main__':
    main()
